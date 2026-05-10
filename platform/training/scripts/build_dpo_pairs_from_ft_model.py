import argparse
import json
import os
import random
import re
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from dotenv import load_dotenv
from openai import AzureOpenAI, BadRequestError

from score_dpo_pairs import eval_side, parse_prompt_context


def read_jsonl(path: Path) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            rows.append(json.loads(line))
    return rows


def append_jsonl(path: Path, row: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")


def load_processed_ids(path: Path) -> set:
    if not path.exists():
        return set()
    ids = set()
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
            except Exception:
                continue
            sid = obj.get("source_id")
            if sid:
                ids.add(sid)
    return ids


def parse_known_issues(prompt: str) -> List[str]:
    m = re.search(r"<KNOWN_ISSUES>(.*?)</KNOWN_ISSUES>", prompt, flags=re.DOTALL)
    if not m:
        return []
    raw = m.group(1).strip()
    try:
        obj = json.loads(raw)
        if isinstance(obj, list):
            return [str(x) for x in obj]
    except Exception:
        pass
    return []


def clean_model_output(raw: str, target_path: str) -> str:
    text = raw.strip()

    if text.startswith("```"):
        text = re.sub(r"^```[a-zA-Z0-9_-]*\n?", "", text)
        text = re.sub(r"\n?```$", "", text).strip()

    try:
        obj = json.loads(text)
        if isinstance(obj, dict) and "path" in obj and "content" in obj:
            return json.dumps(
                {
                    "path": str(obj.get("path", target_path)).strip(),
                    "content": str(obj.get("content", "")),
                },
                ensure_ascii=False,
            )
    except Exception:
        pass

    first = text.find("{")
    last = text.rfind("}")
    if first >= 0 and last > first:
        chunk = text[first : last + 1]
        try:
            obj = json.loads(chunk)
            if isinstance(obj, dict) and "path" in obj and "content" in obj:
                return json.dumps(
                    {
                        "path": str(obj.get("path", target_path)).strip(),
                        "content": str(obj.get("content", "")),
                    },
                    ensure_ascii=False,
                )
        except Exception:
            pass

    return json.dumps({"path": target_path, "content": text}, ensure_ascii=False)


def generate_candidate(
    client: AzureOpenAI,
    model: str,
    system_prompt: str,
    user_prompt: str,
    temperature: float,
    max_tokens: int,
    force_json: bool,
) -> str:
    params: Dict[str, Any] = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        "temperature": temperature,
        "max_tokens": max_tokens,
    }

    if force_json:
        params["response_format"] = {"type": "json_object"}

    try:
        resp = client.chat.completions.create(**params)
    except BadRequestError:
        if "response_format" in params:
            params.pop("response_format")
            resp = client.chat.completions.create(**params)
        else:
            raise

    return (resp.choices[0].message.content or "").strip()


def pick_temperatures(n: int, low: float, high: float) -> List[float]:
    if n <= 1:
        return [low]
    step = (high - low) / max(1, n - 1)
    return [round(low + i * step, 3) for i in range(n)]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", required=True, help="Raw Stage-2 SFT JSONL source")
    ap.add_argument("--spec", required=True, help="Rubric spec JSON path")
    ap.add_argument("--out", required=True, help="Output raw DPO pairs JSONL")
    ap.add_argument("--model", required=True, help="Fine-tuned model id")
    ap.add_argument("--api-version", default="2024-10-21")
    ap.add_argument("--seed", type=int, default=1337)
    ap.add_argument("--max-prompts", type=int, default=160)
    ap.add_argument("--candidates-per-prompt", type=int, default=1)
    ap.add_argument("--temp-low", type=float, default=0.2)
    ap.add_argument("--temp-high", type=float, default=0.8)
    ap.add_argument("--max-tokens", type=int, default=6000)
    ap.add_argument("--max-reference-bytes", type=int, default=20000)
    ap.add_argument("--max-pair-bytes", type=int, default=60000)
    ap.add_argument("--sleep-seconds", type=float, default=0.15)
    ap.add_argument("--force-json", action="store_true")
    args = ap.parse_args()

    base_dir = Path(__file__).resolve().parent.parent
    load_dotenv(base_dir.parent / ".env.development", override=False)
    api_key = os.getenv("AZURE_OPENAI_API_KEY")
    endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    if not api_key or not endpoint:
        raise RuntimeError("Missing AZURE_OPENAI_API_KEY or AZURE_OPENAI_ENDPOINT")

    client = AzureOpenAI(api_key=api_key, azure_endpoint=endpoint, api_version=args.api_version)

    source_path = Path(args.source).resolve()
    spec_path = Path(args.spec).resolve()
    out_path = Path(args.out).resolve()

    spec = json.loads(spec_path.read_text(encoding="utf-8"))
    source_rows = read_jsonl(source_path)

    rng = random.Random(args.seed)
    rng.shuffle(source_rows)

    processed = load_processed_ids(out_path)

    target_total = args.max_prompts if args.max_prompts > 0 else len(source_rows)

    kept = 0
    skipped = 0
    errors = 0

    print("=== BUILD DPO PAIRS FROM FT MODEL ===")
    print(f"source: {source_path}")
    print(f"out:    {out_path}")
    print(f"model:  {args.model}")
    print(f"api:    {args.api_version}")
    print(f"target_prompts: {target_total}")
    print(f"already_processed: {len(processed)}")

    for idx, row in enumerate(source_rows, start=1):
        if kept >= target_total:
            break

        source_id = str(row.get("id", f"row-{idx}"))
        if source_id in processed:
            continue

        system_prompt = str(row.get("system", "")).strip()
        prompt = str(row.get("input", "")).strip()
        reference = str(row.get("output", "")).strip()

        if not system_prompt or not prompt or not reference:
            skipped += 1
            continue

        if len(reference.encode("utf-8")) > args.max_reference_bytes:
            skipped += 1
            continue

        prompt_ctx = parse_prompt_context(prompt)
        target_path = str(row.get("target_path") or prompt_ctx.get("target_file") or "")
        issues = parse_known_issues(prompt)

        try:
            candidates: List[Tuple[str, str, float]] = []  

            ref_eval = eval_side(reference, prompt_ctx, issues, spec)
            candidates.append(("reference", reference, ref_eval.total))

            temps = pick_temperatures(args.candidates_per_prompt, args.temp_low, args.temp_high)
            for t in temps:
                raw = generate_candidate(
                    client=client,
                    model=args.model,
                    system_prompt=system_prompt,
                    user_prompt=prompt,
                    temperature=t,
                    max_tokens=args.max_tokens,
                    force_json=args.force_json,
                )
                cleaned = clean_model_output(raw, target_path)
                ev = eval_side(cleaned, prompt_ctx, issues, spec)
                candidates.append((f"model_t{t}", cleaned, ev.total))
                time.sleep(args.sleep_seconds)

            candidates_sorted = sorted(candidates, key=lambda x: x[2], reverse=True)
            chosen_src, chosen_text, chosen_score = candidates_sorted[0]

            model_candidates = [c for c in candidates_sorted if c[0].startswith("model_")]
            if model_candidates:
                rejected_src, rejected_text, rejected_score = sorted(model_candidates, key=lambda x: x[2])[0]
            else:
                skipped += 1
                continue

            if chosen_text == rejected_text:
                skipped += 1
                continue

            pair_bytes = len((prompt + chosen_text + rejected_text).encode("utf-8"))
            if pair_bytes > args.max_pair_bytes:
                skipped += 1
                continue

            out_row = {
                "id": f"{source_id}::ftpair",
                "source_id": source_id,
                "project": row.get("project"),
                "bucket": row.get("bucket"),
                "stage": "dpo_ft_generated",
                "kind": row.get("kind", "filewise_preference"),
                "variant": row.get("variant", ""),
                "system": system_prompt,
                "prompt": prompt,
                "chosen": chosen_text,
                "rejected": rejected_text,
                "issues": issues,
                "metadata": {
                    "chosen_source": chosen_src,
                    "rejected_source": rejected_src,
                    "chosen_score": round(chosen_score, 4),
                    "rejected_score": round(rejected_score, 4),
                    "candidate_count": len(candidates),
                    "pair_bytes": pair_bytes,
                    "model": args.model,
                },
            }

            append_jsonl(out_path, out_row)
            processed.add(source_id)
            kept += 1

            if kept % 10 == 0:
                print(f"progress: kept={kept} skipped={skipped} errors={errors}")

        except Exception as exc:
            errors += 1
            print(f"[ERROR] {source_id}: {exc}")

    print("\n=== BUILD SUMMARY ===")
    print(f"kept:    {kept}")
    print(f"skipped: {skipped}")
    print(f"errors:  {errors}")
    print(f"output:  {out_path}")


if __name__ == "__main__":
    main()
