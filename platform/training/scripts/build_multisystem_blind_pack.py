import argparse
import itertools
import json
import random
from pathlib import Path
from typing import Dict, List


def has_valid_content_manifest(raw: str, min_files_with_content: int) -> bool:
    try:
        obj = json.loads(raw)
    except Exception:
        return False
    if not isinstance(obj, dict):
        return False
    files = obj.get("files")
    if not isinstance(files, list):
        return False

    count = 0
    for e in files:
        if not isinstance(e, dict):
            continue
        path = str(e.get("path", "")).strip()
        content = e.get("content")
        if path and content is not None and str(content).strip():
            count += 1
    return count >= min_files_with_content


def load_system_file(
    path: Path,
    require_valid_manifest: bool,
    min_files_with_content: int,
) -> Dict[str, Dict[str, str]]:
    """
    Expected JSON format:
    {
      "system": "ai_cdo_dpo",
      "records": [
        {"brief_id":"brief-001","prompt":"...","output":"...","project":"...","bucket":"..."}
      ]
    }
    """
    obj = json.loads(path.read_text(encoding="utf-8"))
    records = obj.get("records", [])
    out: Dict[str, Dict[str, str]] = {}
    for r in records:
        bid = str(r.get("brief_id", "")).strip()
        if not bid:
            continue

        if require_valid_manifest:
            if bool(r.get("valid_manifest", False)) is False:
                continue
            if not has_valid_content_manifest(str(r.get("output", "")), min_files_with_content):
                continue

        out[bid] = {
            "prompt": str(r.get("prompt", "")),
            "output": str(r.get("output", "")),
            "project": str(r.get("project", "")),
            "bucket": str(r.get("bucket", "")),
        }
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--system-json",
        action="append",
        required=True,
        help="Repeatable: name=path_to_system_json",
    )
    ap.add_argument("--seed", type=int, default=1337)
    ap.add_argument("--max-briefs", type=int, default=40)
    ap.add_argument("--require-valid-manifest", action="store_true")
    ap.add_argument("--min-files-with-content", type=int, default=1)
    ap.add_argument("--out-pack", required=True)
    ap.add_argument("--out-key", required=True)
    args = ap.parse_args()

    rng = random.Random(args.seed)

    systems: Dict[str, Dict[str, Dict[str, str]]] = {}
    for item in args.system_json:
        if "=" not in item:
            raise ValueError(f"Invalid --system-json value: {item}. Expected name=path")
        name, p = item.split("=", 1)
        name = name.strip()
        path = Path(p).resolve()
        systems[name] = load_system_file(
            path,
            require_valid_manifest=args.require_valid_manifest,
            min_files_with_content=args.min_files_with_content,
        )

    if len(systems) < 2:
        raise ValueError("Need at least two systems")

    # Intersect briefs across all systems.
    common = None
    for _, recs in systems.items():
        ids = set(recs.keys())
        common = ids if common is None else (common & ids)

    common_ids = sorted(common or [])
    rng.shuffle(common_ids)
    common_ids = common_ids[: args.max_briefs]

    pair_defs = list(itertools.combinations(sorted(systems.keys()), 2))

    pack_briefs: List[Dict[str, object]] = []
    key_rows: List[Dict[str, str]] = []

    idx = 0
    for bid in common_ids:
        base_prompt = ""
        project = ""
        bucket = ""
        for s in systems:
            rec = systems[s][bid]
            if not base_prompt:
                base_prompt = rec.get("prompt", "")
            if not project:
                project = rec.get("project", "")
            if not bucket:
                bucket = rec.get("bucket", "")

        for a_sys, b_sys in pair_defs:
            idx += 1
            rec_a = systems[a_sys][bid]
            rec_b = systems[b_sys][bid]

            if rng.random() < 0.5:
                out_A, out_B = rec_a.get("output", ""), rec_b.get("output", "")
                A_name, B_name = a_sys, b_sys
            else:
                out_A, out_B = rec_b.get("output", ""), rec_a.get("output", "")
                A_name, B_name = b_sys, a_sys

            pair_id = f"{bid}::pair-{idx:03d}"

            pack_briefs.append(
                {
                    "pair_id": pair_id,
                    "brief_id": bid,
                    "project": project,
                    "bucket": bucket,
                    "prompt": base_prompt,
                    "output_A": out_A,
                    "output_B": out_B,
                    "rating_form": {
                        "preferred_output": "A_or_B_or_Equal",
                        "premium_quality_A": "1_to_10",
                        "premium_quality_B": "1_to_10",
                        "business_alignment_A": "1_to_10",
                        "business_alignment_B": "1_to_10",
                        "distinctness_A": "1_to_10",
                        "distinctness_B": "1_to_10",
                        "confidence_collaboration_A": "1_to_10",
                        "confidence_collaboration_B": "1_to_10",
                        "time_to_acceptable_A_min": "float",
                        "time_to_acceptable_B_min": "float",
                        "evaluation_type": "baseline_or_diversity",
                    },
                }
            )
            key_rows.append(
                {
                    "pair_id": pair_id,
                    "brief_id": bid,
                    "A_system": A_name,
                    "B_system": B_name,
                }
            )

    out_pack = Path(args.out_pack).resolve()
    out_key = Path(args.out_key).resolve()
    out_pack.parent.mkdir(parents=True, exist_ok=True)
    out_key.parent.mkdir(parents=True, exist_ok=True)
    out_pack.write_text(json.dumps({"pairs": pack_briefs}, indent=2), encoding="utf-8")
    out_key.write_text(json.dumps({"mapping": key_rows}, indent=2), encoding="utf-8")

    print("=== MULTISYSTEM BLIND PACK ===")
    print(f"systems:       {sorted(systems.keys())}")
    print(f"briefs_common: {len(common_ids)}")
    print(f"pairs_written: {len(pack_briefs)}")
    print(f"pack:          {out_pack}")
    print(f"key:           {out_key}")


if __name__ == "__main__":
    main()
