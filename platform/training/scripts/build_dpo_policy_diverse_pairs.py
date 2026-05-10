import argparse
import json
import random
import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


def read_jsonl(path: Path) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            rows.append(json.loads(line))
    return rows


def write_jsonl(path: Path, rows: List[Dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")


def parse_json_output(text: str) -> Optional[Tuple[str, str]]:
    try:
        obj = json.loads(text)
    except Exception:
        return None
    if not isinstance(obj, dict):
        return None
    p = obj.get("path")
    c = obj.get("content")
    if not isinstance(p, str) or not isinstance(c, str):
        return None
    return p, c


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


def parse_broken_file(prompt: str) -> Optional[str]:
    m = re.search(r"<BROKEN_FILE>(.*?)</BROKEN_FILE>", prompt, flags=re.DOTALL)
    if not m:
        return None
    return m.group(1).strip() or None


def build_bad_rejected_content(seed: int) -> str:
    rng = random.Random(seed)
    noisy_tokens = [
        "ultra", "quantum", "hype", "viral", "blaze", "mega", "instant", "synergy",
        "astral", "hyperloop", "neon", "chaos", "frictionless", "dominance",
    ]
    rng.shuffle(noisy_tokens)
    w = " ".join(noisy_tokens[:6])

    return (
        '"use client"\n\n'
        "export default function AggressiveLanding() {\n"
        "  return (\n"
        "    <section class=\"animate-bounce bg-gradient-to-r from-fuchsia-500 to-cyan-500 transition-all blur-sm\">\n"
        "      <h1>Get started now</h1>\n"
        "      <p>Request demo and contact us today. " + w + "</p>\n"
        "      <button class=\"animate-pulse\">Sign up</button>\n"
        "  )\n"
        "}\n"
    )


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--seed", type=int, default=1337)
    ap.add_argument("--max-pairs", type=int, default=0)
    ap.add_argument("--max-pair-bytes", type=int, default=70000)
    args = ap.parse_args()

    rows = read_jsonl(Path(args.source).resolve())
    rng = random.Random(args.seed)
    rng.shuffle(rows)

    out_rows: List[Dict[str, Any]] = []
    skipped_parse = 0
    skipped_size = 0
    skipped_equal = 0

    for idx, row in enumerate(rows, 1):
        if args.max_pairs > 0 and len(out_rows) >= args.max_pairs:
            break

        parsed = parse_json_output(str(row.get("output", "")))
        if not parsed:
            skipped_parse += 1
            continue

        target_path, chosen_content = parsed
        chosen_text = json.dumps({"path": target_path, "content": chosen_content}, ensure_ascii=False)

        kind_in = str(row.get("kind", ""))
        prompt = str(row.get("input", ""))

        if kind_in == "repair":
            broken = parse_broken_file(prompt)
            rejected_content = broken or build_bad_rejected_content(args.seed + idx * 11)
            out_kind = "repair_preference"
            issues = parse_known_issues(prompt) or ["jsx_attr_regression", "missing_closer"]
        else:
            rejected_content = build_bad_rejected_content(args.seed + idx * 11)
            out_kind = "strategy_diversity_preference"
            issues = ["jsx_attr_regression", "missing_closer"]

        rejected_text = json.dumps({"path": target_path, "content": rejected_content}, ensure_ascii=False)

        if chosen_text == rejected_text:
            skipped_equal += 1
            continue

        pair_bytes = len((prompt + chosen_text + rejected_text).encode("utf-8"))
        if pair_bytes > args.max_pair_bytes:
            skipped_size += 1
            continue

        out_rows.append(
            {
                "id": f"{row.get('id', f'row-{idx}')}::policy_diverse_pref",
                "project": row.get("project"),
                "bucket": row.get("bucket"),
                "stage": "dpo_seed_policy_diverse",
                "kind": out_kind,
                "variant": row.get("variant", ""),
                "system": row.get("system"),
                "prompt": prompt,
                "chosen": chosen_text,
                "rejected": rejected_text,
                "issues": issues,
                "metadata": {
                    "generator": "policy_diverse_rejector",
                    "pair_bytes": pair_bytes,
                    "source_kind": kind_in,
                },
            }
        )

    out_path = Path(args.out).resolve()
    write_jsonl(out_path, out_rows)

    print("=== POLICY DIVERSE DPO SEED SUMMARY ===")
    print(f"source_rows:      {len(rows)}")
    print(f"output_rows:      {len(out_rows)}")
    print(f"skipped_parse:    {skipped_parse}")
    print(f"skipped_size:     {skipped_size}")
    print(f"skipped_equal:    {skipped_equal}")
    print(f"out:              {out_path}")


if __name__ == "__main__":
    main()
