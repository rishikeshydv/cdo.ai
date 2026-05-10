import argparse
import hashlib
import json
from pathlib import Path
from typing import Any, Dict, List


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


def to_preference_row(row: Dict[str, Any], include_system: bool) -> Dict[str, Any]:
    system_text = str(row.get("system", "")).strip()
    prompt = str(row.get("prompt", "")).strip()
    chosen = str(row.get("chosen", "")).strip()
    rejected = str(row.get("rejected", "")).strip()

    input_messages: List[Dict[str, str]] = []
    if include_system and system_text:
        input_messages.append({"role": "system", "content": system_text})
    input_messages.append({"role": "user", "content": prompt})

    return {
        "input": {"messages": input_messages},
        "preferred_output": [{"role": "assistant", "content": chosen}],
        "non_preferred_output": [{"role": "assistant", "content": rejected}],
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True, help="Rubric-gated DPO pairs JSONL")
    ap.add_argument("--output", required=True, help="OpenAI preference-format JSONL")
    ap.add_argument("--max-example-bytes", type=int, default=60000)
    ap.add_argument("--include-system", action="store_true")
    args = ap.parse_args()

    src_rows = read_jsonl(Path(args.input).resolve())

    out_rows: List[Dict[str, Any]] = []
    seen = set()
    skipped_empty = 0
    skipped_size = 0
    skipped_dup = 0

    for row in src_rows:
        prompt = str(row.get("prompt", "")).strip()
        chosen = str(row.get("chosen", "")).strip()
        rejected = str(row.get("rejected", "")).strip()
        if not prompt or not chosen or not rejected:
            skipped_empty += 1
            continue

        converted = to_preference_row(row, include_system=args.include_system)
        blob = json.dumps(converted, ensure_ascii=False)
        if len(blob.encode("utf-8")) > args.max_example_bytes:
            skipped_size += 1
            continue

        h = hashlib.sha256(blob.encode("utf-8")).hexdigest()
        if h in seen:
            skipped_dup += 1
            continue
        seen.add(h)
        out_rows.append(converted)

    out_path = Path(args.output).resolve()
    write_jsonl(out_path, out_rows)

    print("=== OPENAI DPO CONVERSION SUMMARY ===")
    print(f"source_rows:      {len(src_rows)}")
    print(f"output_rows:      {len(out_rows)}")
    print(f"skipped_empty:    {skipped_empty}")
    print(f"skipped_size:     {skipped_size}")
    print(f"skipped_dup:      {skipped_dup}")
    print(f"out:              {out_path}")


if __name__ == "__main__":
    main()
