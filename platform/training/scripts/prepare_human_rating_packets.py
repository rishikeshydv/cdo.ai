import argparse
import csv
from pathlib import Path
from typing import List, Dict, Tuple


def read_table(path: Path) -> Tuple[List[str], List[Dict[str, str]]]:
    with path.open("r", newline="", encoding="utf-8") as f:
        r = csv.DictReader(f)
        fieldnames = list(r.fieldnames or [])
        rows = list(r)
    return fieldnames, rows


def write_table(path: Path, fieldnames: List[str], rows: List[Dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        if not fieldnames:
            return
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        if rows:
            w.writerows(rows)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--ratings-template", required=True)
    ap.add_argument("--h4-template", required=True)
    ap.add_argument("--out-dir", required=True)
    ap.add_argument("--raters", type=int, default=5)
    ap.add_argument("--prefix", default="rater")
    args = ap.parse_args()

    ratings_fields, ratings_rows = read_table(Path(args.ratings_template).resolve())
    h4_fields, h4_rows = read_table(Path(args.h4_template).resolve())

    out_dir = Path(args.out_dir).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    for i in range(1, args.raters + 1):
        rid = f"{args.prefix}_{i:02d}"

        r_rows = [dict(r) for r in ratings_rows]
        for r in r_rows:
            r["rater_id"] = rid
        write_table(out_dir / f"human_pair_ratings_{rid}.csv", ratings_fields, r_rows)

        h_rows = [dict(r) for r in h4_rows]
        for h in h_rows:
            h["rater_id"] = rid
        write_table(out_dir / f"h4_session_{rid}.csv", h4_fields, h_rows)

    print("=== HUMAN RATING PACKETS CREATED ===")
    print(f"raters: {args.raters}")
    print(f"out_dir: {out_dir}")


if __name__ == "__main__":
    main()
