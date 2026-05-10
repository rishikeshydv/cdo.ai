import argparse
import csv
import json
from pathlib import Path
from typing import Dict, List

LONG_FIELDS = [
    "rater_id",
    "pair_id",
    "brief_id",
    "evaluation_type",
    "system",
    "is_preferred",
    "premium_quality",
    "business_alignment",
    "distinctness",
    "confidence_collaboration",
    "time_to_acceptable_min",
    "notes",
]

PAIR_FIELDS = [
    "rater_id",
    "pair_id",
    "brief_id",
    "evaluation_type",
    "system_A",
    "system_B",
    "preferred_output",
    "preferred_system",
]


def parse_num(x: str) -> float:
    try:
        return float(x)
    except Exception:
        return 0.0


def preferred_to_flags(pref: str) -> Dict[str, float]:
    p = (pref or "").strip().lower()
    if p == "a":
        return {"A": 1.0, "B": 0.0}
    if p == "b":
        return {"A": 0.0, "B": 1.0}
    return {"A": 0.5, "B": 0.5}


def row_has_rating_content(row: Dict[str, str]) -> bool:
    fields = [
        "preferred_output",
        "premium_quality_A",
        "premium_quality_B",
        "business_alignment_A",
        "business_alignment_B",
        "distinctness_A",
        "distinctness_B",
        "confidence_collaboration_A",
        "confidence_collaboration_B",
        "time_to_acceptable_A_min",
        "time_to_acceptable_B_min",
        "notes",
    ]
    return any(str(row.get(field, "")).strip() for field in fields)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--ratings-csv", required=True)
    ap.add_argument("--blind-key", required=True)
    ap.add_argument("--out-long-csv", default="")
    ap.add_argument("--out-pair-csv", default="")
    # Backward-compatible aliases used in earlier runs.
    ap.add_argument("--out-long", default="")
    ap.add_argument("--out-pair", default="")
    args = ap.parse_args()

    long_raw = args.out_long_csv or args.out_long
    pair_raw = args.out_pair_csv or args.out_pair
    if not long_raw or not pair_raw:
        raise ValueError("Provide --out-long-csv/--out-pair-csv (or legacy --out-long/--out-pair).")

    ratings_path = Path(args.ratings_csv).resolve()
    key_path = Path(args.blind_key).resolve()
    out_long = Path(long_raw).resolve()
    out_pair = Path(pair_raw).resolve()

    key_obj = json.loads(key_path.read_text(encoding="utf-8"))
    mapping_rows = key_obj.get("mapping", [])
    map_by_pair = {m.get("pair_id", ""): m for m in mapping_rows if m.get("pair_id")}
    map_by_brief = {m.get("brief_id", ""): m for m in mapping_rows if m.get("brief_id")}

    rows: List[Dict[str, str]] = []
    with ratings_path.open("r", newline="", encoding="utf-8") as f:
        r = csv.DictReader(f)
        for row in r:
            rows.append(row)

    long_rows: List[Dict[str, object]] = []
    pair_rows: List[Dict[str, object]] = []

    for row in rows:
        if not row_has_rating_content(row):
            continue

        pair_id = row.get("pair_id", "") or row.get("brief_id", "")
        brief_id = row.get("brief_id", "")

        m = map_by_pair.get(pair_id) or map_by_brief.get(brief_id)
        if not m:
            continue

        a_system = m.get("A_system", "A_unknown")
        b_system = m.get("B_system", "B_unknown")
        pref = preferred_to_flags(row.get("preferred_output", ""))

        base = {
            "rater_id": row.get("rater_id", ""),
            "pair_id": pair_id,
            "brief_id": brief_id or m.get("brief_id", ""),
            "evaluation_type": row.get("evaluation_type", "baseline"),
        }

        a_rec = {
            **base,
            "system": a_system,
            "is_preferred": pref["A"],
            "premium_quality": parse_num(row.get("premium_quality_A", "")),
            "business_alignment": parse_num(row.get("business_alignment_A", "")),
            "distinctness": parse_num(row.get("distinctness_A", "")),
            "confidence_collaboration": parse_num(row.get("confidence_collaboration_A", "")),
            "time_to_acceptable_min": parse_num(row.get("time_to_acceptable_A_min", "")),
            "notes": row.get("notes", ""),
        }
        b_rec = {
            **base,
            "system": b_system,
            "is_preferred": pref["B"],
            "premium_quality": parse_num(row.get("premium_quality_B", "")),
            "business_alignment": parse_num(row.get("business_alignment_B", "")),
            "distinctness": parse_num(row.get("distinctness_B", "")),
            "confidence_collaboration": parse_num(row.get("confidence_collaboration_B", "")),
            "time_to_acceptable_min": parse_num(row.get("time_to_acceptable_B_min", "")),
            "notes": row.get("notes", ""),
        }
        long_rows.extend([a_rec, b_rec])

        pair_rows.append(
            {
                **base,
                "system_A": a_system,
                "system_B": b_system,
                "preferred_output": row.get("preferred_output", ""),
                "preferred_system": a_system if pref["A"] > pref["B"] else b_system if pref["B"] > pref["A"] else "Equal",
            }
        )

    out_long.parent.mkdir(parents=True, exist_ok=True)
    with out_long.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=LONG_FIELDS)
        w.writeheader()
        if long_rows:
            w.writerows(long_rows)

    out_pair.parent.mkdir(parents=True, exist_ok=True)
    with out_pair.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=PAIR_FIELDS)
        w.writeheader()
        if pair_rows:
            w.writerows(pair_rows)

    print("=== BLIND RATINGS DECODED ===")
    print(f"ratings_rows: {len(rows)}")
    print(f"long_rows:    {len(long_rows)}")
    print(f"pair_rows:    {len(pair_rows)}")
    print(f"out_long:     {out_long}")
    print(f"out_pair:     {out_pair}")


if __name__ == "__main__":
    main()
