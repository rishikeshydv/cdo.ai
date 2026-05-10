import argparse
import json
import re
from pathlib import Path
from typing import Any, Dict, List, Tuple


def safe_slug(text: str) -> str:
    s = re.sub(r"[^a-zA-Z0-9._-]+", "-", text.strip())
    s = s.strip("-")
    return s or "pair"


def parse_manifest(raw: str) -> Tuple[Dict[str, Any], str]:
    try:
        obj = json.loads(raw)
    except Exception as exc:
        return {}, f"json_parse_error: {exc}"

    if not isinstance(obj, dict):
        return {}, "manifest_not_object"
    files = obj.get("files")
    if not isinstance(files, list):
        return {}, "manifest_missing_files"

    return obj, ""


def write_manifest_project(manifest: Dict[str, Any], target_root: Path) -> None:
    files = manifest.get("files", [])
    target_root.mkdir(parents=True, exist_ok=True)

    for entry in files:
        rel_path = str(entry.get("path", "")).strip()
        content = entry.get("content")
        if not rel_path or content is None:
            continue

        full = (target_root / rel_path).resolve()
        if target_root not in full.parents and full != target_root:
            raise ValueError(f"Refusing to write outside target root: {full}")

        full.parent.mkdir(parents=True, exist_ok=True)
        full.write_text(str(content), encoding="utf-8")



def write_side(
    pair: Dict[str, Any],
    side: str,
    side_dir: Path,
    overwrite: bool,
) -> Dict[str, Any]:
    side_dir = side_dir.resolve()
    side_dir.mkdir(parents=True, exist_ok=True)

    raw = str(pair.get(f"output_{side}", ""))
    manifest, err = parse_manifest(raw)

    meta = {
        "pair_id": pair.get("pair_id", ""),
        "brief_id": pair.get("brief_id", ""),
        "side": side,
        "project": pair.get("project", ""),
        "bucket": pair.get("bucket", ""),
        "parse_error": err,
        "is_runnable_manifest": not bool(err),
        "instructions": manifest.get("instructions", "") if manifest else "",
    }

    # Always keep prompt and raw output for audit.
    (side_dir / "_prompt.txt").write_text(str(pair.get("prompt", "")), encoding="utf-8")
    (side_dir / "_output_raw.json.txt").write_text(raw, encoding="utf-8")
    (side_dir / "_meta.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")

    if err:
        return meta

    if overwrite:
        for p in side_dir.glob("**/*"):
            if p.is_file() and p.name not in {"_prompt.txt", "_output_raw.json.txt", "_meta.json"}:
                p.unlink()

    write_manifest_project(manifest, side_dir)
    return meta


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--blind-pack", required=True)
    ap.add_argument("--out-root", required=True)
    ap.add_argument("--pair-id", default="", help="Render one pair by pair_id")
    ap.add_argument("--pair-index", type=int, default=0, help="1-based index if pair-id not given")
    ap.add_argument("--all", action="store_true", help="Render all pairs")
    ap.add_argument("--only-valid", action="store_true", help="With --all, only render pairs where both A/B parse")
    ap.add_argument("--overwrite", action="store_true")
    args = ap.parse_args()

    pack_path = Path(args.blind_pack).resolve()
    out_root = Path(args.out_root).resolve()
    data = json.loads(pack_path.read_text(encoding="utf-8"))
    pairs = data.get("pairs", data.get("briefs", []))

    selected: List[Dict[str, Any]] = []
    if args.all:
        selected = list(pairs)
    elif args.pair_id:
        selected = [p for p in pairs if str(p.get("pair_id", "")) == args.pair_id]
    elif args.pair_index > 0:
        idx = args.pair_index - 1
        if idx < 0 or idx >= len(pairs):
            raise IndexError(f"pair-index out of range: {args.pair_index}")
        selected = [pairs[idx]]
    else:
        raise ValueError("Provide one of --all, --pair-id, or --pair-index")

    out_root.mkdir(parents=True, exist_ok=True)
    rendered = 0
    skipped = 0
    invalid = 0

    for pair in selected:
        pair_id = str(pair.get("pair_id", "")) or f"pair-{rendered+1:03d}"
        pair_dir = out_root / safe_slug(pair_id)

        # Pre-check validity if requested.
        if args.only_valid:
            _, err_a = parse_manifest(str(pair.get("output_A", "")))
            _, err_b = parse_manifest(str(pair.get("output_B", "")))
            if err_a or err_b:
                skipped += 1
                continue

        meta_a = write_side(pair, "A", pair_dir / "A", overwrite=args.overwrite)
        meta_b = write_side(pair, "B", pair_dir / "B", overwrite=args.overwrite)

        if meta_a.get("parse_error") or meta_b.get("parse_error"):
            invalid += 1

        rendered += 1

    print("=== BLIND PAIR PROJECTS RENDERED ===")
    print(f"pack:          {pack_path}")
    print(f"out_root:      {out_root}")
    print(f"requested:     {len(selected)}")
    print(f"rendered:      {rendered}")
    print(f"invalid_pairs: {invalid}")
    print(f"skipped:       {skipped}")


if __name__ == "__main__":
    main()
