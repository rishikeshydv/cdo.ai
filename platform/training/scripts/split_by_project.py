import argparse
import ast
import json
import random
from collections import defaultdict
from pathlib import Path


def _parse_record(line: str):
    """Parse JSON; fall back to Python literal eval for single-quoted records."""
    try:
        return json.loads(line)
    except json.JSONDecodeError:
        try:
            return ast.literal_eval(line)
        except Exception:
            return None

def main():
    ap = argparse.ArgumentParser()
    default_in = Path(__file__).resolve().parent.parent / "data" / "sft_raw_jsonl"
    ap.add_argument("--in_jsonl", default=str(default_in))
    ap.add_argument("--out_train", required=True)
    ap.add_argument("--out_val", required=True)
    ap.add_argument("--val_ratio", type=float, default=0.1)
    ap.add_argument("--seed", type=int, default=1337)
    args = ap.parse_args()

    by_project = defaultdict(list)

    with open(args.in_jsonl, "r", encoding="utf-8") as f:
        for line in f:
            rec = _parse_record(line)
            if not rec or "project" not in rec:
                continue
            by_project[rec["project"]].append(rec)

    projects = sorted(by_project.keys())
    rng = random.Random(args.seed)
    rng.shuffle(projects)

    val_n = max(1, int(len(projects) * args.val_ratio))
    val_projects = set(projects[:val_n])

    train_count = 0
    val_count = 0

    with open(args.out_train, "w", encoding="utf-8") as ftrain, open(args.out_val, "w", encoding="utf-8") as fval:
        for p in projects:
            target = fval if p in val_projects else ftrain
            for rec in by_project[p]:
                target.write(json.dumps(rec, ensure_ascii=False) + "\n")
            if p in val_projects:
                val_count += len(by_project[p])
            else:
                train_count += len(by_project[p])

    print("\n=== SPLIT SUMMARY ===")
    print(f"projects_total: {len(projects)}")
    print(f"projects_val:   {len(val_projects)}")
    print(f"rows_train:     {train_count}")
    print(f"rows_val:       {val_count}")

if __name__ == "__main__":
    main()


# python3 split_by_project.py \
#   --in_jsonl ../data/sft_data.jsonl \
#   --out_train ../data/sft_train.jsonl \
#   --out_val ../data/sft_val.jsonl \
#   --val_ratio 0.1 \
#   --seed 1337
