import argparse
import csv
import glob
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


def resolve_glob(pattern: str) -> List[Path]:
    return [Path(p).resolve() for p in sorted(glob.glob(pattern))]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--ratings-glob", required=True, help="Glob for per-rater pair rating CSVs")
    ap.add_argument("--h4-glob", required=True, help="Glob for per-rater H4 CSVs")
    ap.add_argument("--out-ratings", required=True)
    ap.add_argument("--out-h4", required=True)
    args = ap.parse_args()

    ratings_files = resolve_glob(args.ratings_glob)
    h4_files = resolve_glob(args.h4_glob)

    ratings_fields: List[str] = []
    ratings_rows: List[Dict[str, str]] = []
    for p in ratings_files:
        fields, rows = read_table(p.resolve())
        if not ratings_fields and fields:
            ratings_fields = fields
        ratings_rows.extend(rows)

    h4_fields: List[str] = []
    h4_rows: List[Dict[str, str]] = []
    for p in h4_files:
        fields, rows = read_table(p.resolve())
        if not h4_fields and fields:
            h4_fields = fields
        h4_rows.extend(rows)

    write_table(Path(args.out_ratings).resolve(), ratings_fields, ratings_rows)
    write_table(Path(args.out_h4).resolve(), h4_fields, h4_rows)

    print("=== HUMAN RATING PACKETS MERGED ===")
    print(f"ratings_files: {len(ratings_files)}")
    print(f"h4_files: {len(h4_files)}")
    print(f"out_ratings: {Path(args.out_ratings).resolve()}")
    print(f"out_h4: {Path(args.out_h4).resolve()}")


if __name__ == "__main__":
    main()
