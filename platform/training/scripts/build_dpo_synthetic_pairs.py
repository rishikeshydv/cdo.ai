import argparse
import json
import random
import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from build_multistage_sft_dataset import make_corrupted_content


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
    content = m.group(1).strip()
    return content if content else None


def parse_file_output(text: str) -> Optional[Tuple[str, str]]:
    try:
        obj = json.loads(text)
    except Exception:
        return None

    if not isinstance(obj, dict):
        return None
    path = obj.get("path")
    content = obj.get("content")
    if not isinstance(path, str) or not isinstance(content, str):
        return None
    return path, content


def build_rejected(
    row: Dict[str, Any],
    chosen_path: str,
    chosen_content: str,
    seed: int,
) -> Tuple[str, List[str]]:
    prompt = str(row.get("input", ""))
    known_issues = parse_known_issues(prompt)

    if str(row.get("kind", "")) == "repair":
        broken = parse_broken_file(prompt)
        if broken:
            return broken, known_issues

    broken, issues = make_corrupted_content(chosen_content, seed=seed)
    return broken, (known_issues or issues)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", required=True, help="sft_stage2_filewise_train.jsonl")
    ap.add_argument("--out", required=True, help="Output DPO seed JSONL")
    ap.add_argument("--seed", type=int, default=1337)
    ap.add_argument("--max-pairs", type=int, default=0, help="0 means all")
    ap.add_argument("--max-chosen-bytes", type=int, default=30000)
    ap.add_argument("--max-pair-bytes", type=int, default=70000)
    args = ap.parse_args()

    rows = read_jsonl(Path(args.source).resolve())
    rng = random.Random(args.seed)
    rng.shuffle(rows)

    out_rows: List[Dict[str, Any]] = []
    skipped_parse = 0
    skipped_size = 0
    skipped_equal = 0

    for idx, row in enumerate(rows):
        if args.max_pairs > 0 and len(out_rows) >= args.max_pairs:
            break

        output = str(row.get("output", ""))
        parsed = parse_file_output(output)
        if not parsed:
            skipped_parse += 1
            continue

        chosen_path, chosen_content = parsed
        chosen_obj = {"path": chosen_path, "content": chosen_content}
        chosen_text = json.dumps(chosen_obj, ensure_ascii=False)

        if len(chosen_text.encode("utf-8")) > args.max_chosen_bytes:
            skipped_size += 1
            continue

        rejected_content, issues = build_rejected(
            row=row,
            chosen_path=chosen_path,
            chosen_content=chosen_content,
            seed=args.seed + idx * 17 + 11,
        )
        rejected_obj = {"path": chosen_path, "content": rejected_content}
        rejected_text = json.dumps(rejected_obj, ensure_ascii=False)

        if chosen_text == rejected_text:
            skipped_equal += 1
            continue

        pair_bytes = len((str(row.get("input", "")) + chosen_text + rejected_text).encode("utf-8"))
        if pair_bytes > args.max_pair_bytes:
            skipped_size += 1
            continue

        out_rows.append(
            {
                "id": f"{row.get('id', f'row-{idx+1}')}::synthetic_pref",
                "project": row.get("project"),
                "bucket": row.get("bucket"),
                "stage": "dpo_seed_synthetic",
                "kind": row.get("kind", "filewise_preference"),
                "variant": row.get("variant", ""),
                "system": row.get("system"),
                "prompt": row.get("input"),
                "chosen": chosen_text,
                "rejected": rejected_text,
                "issues": issues,
                "metadata": {
                    "generator": "synthetic_corruption",
                    "pair_bytes": pair_bytes,
                },
            }
        )

    out_path = Path(args.out).resolve()
    write_jsonl(out_path, out_rows)

    print("=== SYNTHETIC DPO SEED SUMMARY ===")
    print(f"source_rows:      {len(rows)}")
    print(f"output_rows:      {len(out_rows)}")
    print(f"skipped_parse:    {skipped_parse}")
    print(f"skipped_size:     {skipped_size}")
    print(f"skipped_equal:    {skipped_equal}")
    print(f"out:              {out_path}")


if __name__ == "__main__":
    main()
