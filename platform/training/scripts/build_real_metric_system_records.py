import argparse
import json
import os
import random
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from dotenv import load_dotenv
import requests


STRICT_SUFFIX = (
    "\n\n<STRICT_OUTPUT_FORMAT>\n"
    "Return VALID JSON only."
    " The JSON must be an object with key 'files' (array) and optional 'instructions'."
    " Each files[] item must include: 'path' (string) and 'content' (full file text string)."
    " Do NOT output placeholders like 'purpose'."
    " Do NOT output markdown fences."
)


def read_jsonl(path: Path) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def parse_models(items: List[str]) -> List[Tuple[str, str]]:
    out: List[Tuple[str, str]] = []
    for raw in items:
        if "=" not in raw:
            raise ValueError(f"Invalid --model '{raw}'. Expected system_name=model_id")
        name, model = raw.split("=", 1)
        name = name.strip()
        model = model.strip()
        if not name or not model:
            raise ValueError(f"Invalid --model '{raw}'. Expected system_name=model_id")
        out.append((name, model))
    if len(out) < 2:
        raise ValueError("Provide at least two --model entries")
    return out


def load_existing_records(path: Path) -> Dict[str, Dict[str, Any]]:
    if not path.exists():
        return {}
    obj = json.loads(path.read_text(encoding="utf-8"))
    records = obj.get("records", []) if isinstance(obj, dict) else []
    out: Dict[str, Dict[str, Any]] = {}
    for r in records:
        bid = str(r.get("brief_id", "")).strip()
        if bid:
            out[bid] = r
    return out


def choose_briefs(rows: List[Dict[str, Any]], max_briefs: int, seed: int) -> List[Dict[str, Any]]:
    usable = [r for r in rows if str(r.get("input", "")).strip() and str(r.get("system", "")).strip()]
    rng = random.Random(seed)
    rng.shuffle(usable)
    selected = usable[: min(max_briefs, len(usable))]

    out: List[Dict[str, Any]] = []
    for i, r in enumerate(selected, 1):
        out.append(
            {
                "brief_id": f"brief-{i:03d}",
                "source_id": str(r.get("id", f"row-{i}")),
                "project": str(r.get("project", "")),
                "bucket": str(r.get("bucket", "")),
                "system_prompt": str(r.get("system", "")),
                "input_prompt": str(r.get("input", "")),
            }
        )
    return out


def load_selected_briefs(path: Path, max_briefs: int) -> List[Dict[str, Any]]:
    obj = json.loads(path.read_text(encoding="utf-8"))
    briefs = obj.get("briefs", [])
    if not isinstance(briefs, list):
        raise ValueError(f"selected-briefs file invalid: {path}")
    out = briefs[: min(max_briefs, len(briefs))]
    for b in out:
        for key in ["brief_id", "source_id", "project", "bucket", "system_prompt", "input_prompt"]:
            if key not in b:
                raise ValueError(f"selected brief missing key '{key}': {b}")
    return out


def write_system_records(path: Path, system_name: str, records_by_brief: Dict[str, Dict[str, Any]]) -> None:
    ordered = [records_by_brief[k] for k in sorted(records_by_brief.keys())]
    payload = {"system": system_name, "records": ordered}
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def extract_json_candidate(raw: str) -> Optional[str]:
    text = raw.strip()
    if not text:
        return None

    if text.startswith("```"):
        text = text.strip("`")
        lines = text.splitlines()
        if lines and lines[0].strip().lower().startswith("json"):
            lines = lines[1:]
        text = "\n".join(lines).strip()

    try:
        json.loads(text)
        return text
    except Exception:
        pass

    start = text.find("{")
    end = text.rfind("}")
    if start >= 0 and end > start:
        sub = text[start : end + 1]
        try:
            json.loads(sub)
            return sub
        except Exception:
            return None
    return None


def normalize_manifest_obj(obj: Dict[str, Any]) -> Dict[str, Any]:
    files = obj.get("files")
    out_files: List[Dict[str, str]] = []

    if isinstance(files, list):
        for e in files:
            if not isinstance(e, dict):
                continue
            path = str(e.get("path", "")).strip()
            content = e.get("content")
            if not path or content is None:
                continue
            out_files.append({"path": path, "content": str(content)})
    elif "path" in obj and "content" in obj:
        path = str(obj.get("path", "")).strip()
        content = obj.get("content")
        if path and content is not None:
            out_files.append({"path": path, "content": str(content)})

    norm = {"files": out_files}
    inst = obj.get("instructions")
    if isinstance(inst, str) and inst.strip():
        norm["instructions"] = inst
    return norm


def parse_and_validate_manifest(raw: str, min_files_with_content: int) -> Tuple[Optional[str], int, str]:
    cand = extract_json_candidate(raw)
    if not cand:
        return None, 0, "json_parse_error"

    try:
        obj = json.loads(cand)
    except Exception as exc:
        return None, 0, f"json_parse_error:{exc}"

    if not isinstance(obj, dict):
        return None, 0, "manifest_not_object"

    norm = normalize_manifest_obj(obj)
    files = norm.get("files", [])
    content_count = len([f for f in files if str(f.get("content", "")).strip()])
    if content_count < min_files_with_content:
        return None, content_count, f"insufficient_file_content:{content_count}"

    return json.dumps(norm, ensure_ascii=False), content_count, ""


def generate_once(
    azure_endpoint: str,
    azure_api_key: str,
    api_version: str,
    model_id: str,
    system_prompt: str,
    user_prompt: str,
    temperature: float,
    max_tokens: int,
    try_response_format: bool,
    request_timeout_seconds: float,
) -> str:
    url = f"{azure_endpoint.rstrip('/')}/openai/deployments/{model_id}/chat/completions"
    params = {"api-version": api_version}
    headers = {"api-key": azure_api_key, "Content-Type": "application/json"}
    payload: Dict[str, Any] = {
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        "temperature": temperature,
        "max_tokens": max_tokens,
    }

    if try_response_format:
        payload["response_format"] = {"type": "json_object"}

    response = requests.post(
        url,
        params=params,
        headers=headers,
        json=payload,
        timeout=request_timeout_seconds if request_timeout_seconds > 0 else None,
    )

    if response.status_code >= 400 and try_response_format:
        payload.pop("response_format", None)
        response = requests.post(
            url,
            params=params,
            headers=headers,
            json=payload,
            timeout=request_timeout_seconds if request_timeout_seconds > 0 else None,
        )

    if response.status_code >= 400:
        raise RuntimeError(f"http_{response.status_code}:{response.text[:400]}")

    data = response.json()
    choices = data.get("choices") if isinstance(data, dict) else None
    if not isinstance(choices, list) or not choices:
        raise RuntimeError("invalid_response_no_choices")

    message = choices[0].get("message", {}) if isinstance(choices[0], dict) else {}
    content = message.get("content", "")
    return str(content).strip()


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--eval-jsonl", required=True)
    ap.add_argument("--selected-briefs-json", default="")
    ap.add_argument("--model", action="append", required=True, help="Repeatable: system_name=model_id")
    ap.add_argument("--out-dir", required=True)
    ap.add_argument("--max-briefs", type=int, default=40)
    ap.add_argument("--seed", type=int, default=1337)
    ap.add_argument("--temperature", type=float, default=0.2)
    ap.add_argument("--max-tokens", type=int, default=6000)
    ap.add_argument("--request-timeout-seconds", type=float, default=120.0)
    ap.add_argument("--sleep-seconds", type=float, default=0.15)
    ap.add_argument("--api-version", default="")
    ap.add_argument("--resume", action="store_true")
    ap.add_argument("--resume-repair-invalid", action="store_true")
    ap.add_argument("--max-retries", type=int, default=4)
    ap.add_argument("--min-files-with-content", type=int, default=1)
    ap.add_argument("--strict-output", action="store_true")
    ap.add_argument("--try-response-format", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    eval_path = Path(args.eval_jsonl).resolve()
    out_dir = Path(args.out_dir).resolve()

    models = parse_models(args.model)
    rows = read_jsonl(eval_path)

    if args.selected_briefs_json:
        briefs = load_selected_briefs(Path(args.selected_briefs_json).resolve(), args.max_briefs)
    else:
        briefs = choose_briefs(rows, args.max_briefs, args.seed)

    out_dir.mkdir(parents=True, exist_ok=True)
    briefs_path = out_dir / "selected_briefs.json"
    briefs_path.write_text(json.dumps({"briefs": briefs}, indent=2), encoding="utf-8")

    api_key = ""
    endpoint = ""
    api_version = args.api_version or "2024-10-21"
    if not args.dry_run:
        script_dir = Path(__file__).resolve().parent
        training_dir = script_dir.parent
        platform_dir = training_dir.parent
        root_dir = platform_dir.parent
        load_dotenv(platform_dir / ".env.development", override=False)
        load_dotenv(root_dir / ".env.development", override=False)

        api_key = os.getenv("AZURE_OPENAI_API_KEY")
        endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
        api_version = args.api_version or os.getenv("AZURE_OPENAI_API_VERSION") or "2024-10-21"
        if not api_key or not endpoint:
            raise RuntimeError("Missing AZURE_OPENAI_API_KEY or AZURE_OPENAI_ENDPOINT")

    print("=== BUILD REAL METRIC SYSTEM RECORDS ===")
    print(f"eval_rows:    {len(rows)}")
    print(f"briefs_used:  {len(briefs)}")
    print(f"out_dir:      {out_dir}")
    print(f"dry_run:      {args.dry_run}")

    for system_name, model_id in models:
        out_path = out_dir / f"{system_name}_records.json"
        existing = load_existing_records(out_path) if args.resume else {}

        kept = 0
        skipped = 0
        errors = 0
        repaired = 0

        print(f"\n[system={system_name}] model={model_id}")
        print(f"existing_records: {len(existing)}")

        for idx, b in enumerate(briefs, 1):
            bid = b["brief_id"]

            if bid in existing:
                if args.resume_repair_invalid:
                    rec = existing[bid]
                    if bool(rec.get("valid_manifest", False)):
                        skipped += 1
                        continue
                    repaired += 1
                else:
                    skipped += 1
                    continue

            try:
                if args.dry_run:
                    output_text = (
                        '{"files":[{"path":"src/app/page.tsx","content":"// dry run output"}],"instructions":"npm run dev"}'
                    )
                    manifest_text, content_count, val_err = parse_and_validate_manifest(
                        output_text, args.min_files_with_content
                    )
                    valid = manifest_text is not None
                    final_out = manifest_text or output_text
                    attempts = 1
                    last_err = val_err
                else:
                    valid = False
                    final_out = ""
                    content_count = 0
                    attempts = 0
                    last_err = ""

                    base_user = b["input_prompt"]
                    strict_user = base_user + STRICT_SUFFIX if args.strict_output else base_user

                    for attempt in range(1, args.max_retries + 1):
                        attempts = attempt
                        user_prompt = strict_user if args.strict_output else base_user
                        if not args.strict_output and attempt > 1:
                            user_prompt = strict_user
                        try:
                            raw = generate_once(
                                azure_endpoint=endpoint,
                                azure_api_key=api_key,
                                api_version=api_version,
                                model_id=model_id,
                                system_prompt=b["system_prompt"],
                                user_prompt=user_prompt,
                                temperature=args.temperature,
                                max_tokens=args.max_tokens,
                                try_response_format=args.try_response_format,
                                request_timeout_seconds=args.request_timeout_seconds,
                            )
                        except Exception as exc:
                            last_err = f"request_error:{type(exc).__name__}:{exc}"
                            time.sleep(args.sleep_seconds)
                            continue

                        manifest_text, content_count, val_err = parse_and_validate_manifest(
                            raw, args.min_files_with_content
                        )
                        if manifest_text is not None:
                            valid = True
                            final_out = manifest_text
                            last_err = ""
                            break

                        last_err = val_err
                        time.sleep(args.sleep_seconds)

                    if not valid:
                        final_out = raw if 'raw' in locals() else ""

                existing[bid] = {
                    "brief_id": bid,
                    "source_id": b["source_id"],
                    "prompt": b["input_prompt"],
                    "output": final_out,
                    "project": b["project"],
                    "bucket": b["bucket"],
                    "valid_manifest": valid,
                    "files_with_content": content_count,
                    "attempts": attempts,
                    "validation_error": last_err,
                }
                kept += 1

                if kept % 5 == 0 or idx == len(briefs):
                    write_system_records(out_path, system_name, existing)
                    print(
                        f"progress: kept={kept} skipped={skipped} repaired={repaired} errors={errors} ({idx}/{len(briefs)})"
                    )

                if not args.dry_run:
                    time.sleep(args.sleep_seconds)

            except Exception as exc:
                errors += 1
                print(f"[ERROR] brief_id={bid}: {exc}")

        write_system_records(out_path, system_name, existing)
        valid_n = len([1 for r in existing.values() if bool(r.get("valid_manifest", False))])
        print(f"saved: {out_path}")
        print(
            f"summary: kept={kept} skipped={skipped} repaired={repaired} errors={errors} total_saved={len(existing)} valid={valid_n}"
        )

    print("\n=== DONE ===")
    print(f"selected_briefs: {briefs_path}")


if __name__ == "__main__":
    main()
