import argparse
import csv
import json
from pathlib import Path

RATING_FIELDS = [
    "rater_id",
    "pair_id",
    "brief_id",
    "preferred_output",  # A / B / Equal
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
    "evaluation_type",  # baseline / diversity / rationale_on / rationale_off
    "notes",
]

H4_FIELDS = [
    "rater_id",
    "brief_id",
    "confidence_rationale_on",
    "confidence_rationale_off",
    "collaboration_rationale_on",
    "collaboration_rationale_off",
    "notes",
]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--blind-pack", required=True)
    ap.add_argument("--out-ratings-csv", default="")
    ap.add_argument("--out-h4-csv", default="")
    # Backward-compatible aliases used in earlier runs.
    ap.add_argument("--out-ratings", default="")
    ap.add_argument("--out-h4", default="")
    args = ap.parse_args()

    pack_path = Path(args.blind_pack).resolve()
    ratings_raw = args.out_ratings_csv or args.out_ratings
    h4_raw = args.out_h4_csv or args.out_h4
    if not ratings_raw or not h4_raw:
        raise ValueError("Provide --out-ratings-csv/--out-h4-csv (or legacy --out-ratings/--out-h4).")

    out_ratings = Path(ratings_raw).resolve()
    out_h4 = Path(h4_raw).resolve()

    data = json.loads(pack_path.read_text(encoding="utf-8"))
    items = data.get("pairs", data.get("briefs", []))

    out_ratings.parent.mkdir(parents=True, exist_ok=True)
    with out_ratings.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=RATING_FIELDS)
        w.writeheader()
        for b in items:
            w.writerow(
                {
                    "rater_id": "",
                    "pair_id": b.get("pair_id", b.get("brief_id", "")),
                    "brief_id": b.get("brief_id", ""),
                    "preferred_output": "",
                    "premium_quality_A": "",
                    "premium_quality_B": "",
                    "business_alignment_A": "",
                    "business_alignment_B": "",
                    "distinctness_A": "",
                    "distinctness_B": "",
                    "confidence_collaboration_A": "",
                    "confidence_collaboration_B": "",
                    "time_to_acceptable_A_min": "",
                    "time_to_acceptable_B_min": "",
                    "evaluation_type": "baseline",
                    "notes": "",
                }
            )

    # Seed one H4 row per unique brief_id in the pack.
    brief_ids = sorted({str(b.get("brief_id", "")).strip() for b in items if str(b.get("brief_id", "")).strip()})

    out_h4.parent.mkdir(parents=True, exist_ok=True)
    with out_h4.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=H4_FIELDS)
        w.writeheader()
        for bid in brief_ids:
            w.writerow(
                {
                    "rater_id": "",
                    "brief_id": bid,
                    "confidence_rationale_on": "",
                    "confidence_rationale_off": "",
                    "collaboration_rationale_on": "",
                    "collaboration_rationale_off": "",
                    "notes": "",
                }
            )

    print("=== REAL METRIC TEMPLATES GENERATED ===")
    print(f"items_in_pack: {len(items)}")
    print(f"h4_rows:       {len(brief_ids)}")
    print(f"ratings_csv:   {out_ratings}")
    print(f"h4_csv:        {out_h4}")


if __name__ == "__main__":
    main()
