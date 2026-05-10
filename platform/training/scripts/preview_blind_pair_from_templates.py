import argparse
import json
import shutil
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


IGNORE_DIRS = {".git", "node_modules", ".next", "dist", "build", "coverage", "__pycache__"}


def load_pack(path: Path) -> List[Dict[str, Any]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    return data.get("pairs", data.get("briefs", []))


def find_template_project(templates_root: Path, project_name: str) -> Optional[Path]:
    for cat in templates_root.glob("category-*"):
        if not cat.is_dir():
            continue
        candidate = cat / project_name
        if candidate.is_dir():
            return candidate
    return None


def parse_manifest_files(raw: str) -> Tuple[List[Tuple[str, str]], str]:
    try:
        obj = json.loads(raw)
    except Exception as exc:
        return [], f"json_parse_error: {exc}"

    if not isinstance(obj, dict):
        return [], "manifest_not_object"

    files = obj.get("files")
    if not isinstance(files, list):
        return [], "manifest_missing_files"

    patches: List[Tuple[str, str]] = []
    for e in files:
        if not isinstance(e, dict):
            continue
        path = str(e.get("path", "")).strip()
        content = e.get("content")
        if not path or content is None:
            continue
        patches.append((path, str(content)))

    if not patches:
        return [], "manifest_has_no_file_content"

    return patches, ""


def copy_template(src: Path, dst: Path, overwrite: bool) -> None:
    if dst.exists() and overwrite:
        shutil.rmtree(dst)
    dst.mkdir(parents=True, exist_ok=True)

    def _ignore(_dirpath: str, names: List[str]) -> List[str]:
        return [n for n in names if n in IGNORE_DIRS]

    shutil.copytree(src, dst, dirs_exist_ok=True, ignore=_ignore)


def apply_patches(dst_root: Path, patches: List[Tuple[str, str]]) -> int:
    count = 0
    for rel, content in patches:
        full = (dst_root / rel).resolve()
        if dst_root not in full.parents and full != dst_root:
            raise ValueError(f"Refusing to write outside target root: {full}")
        full.parent.mkdir(parents=True, exist_ok=True)
        full.write_text(content, encoding="utf-8")
        count += 1
    return count


def read_text_if_exists(path: Path) -> Optional[str]:
    if not path.exists():
        return None
    try:
        return path.read_text(encoding="utf-8")
    except Exception:
        return None


def ensure_globals_css_compat(project_root: Path) -> List[str]:
    """
    Some generated layouts import '@/styles/globals.css', but many templates only
    have app globals at app/globals.css or src/app/globals.css.
    Create missing styles/globals.css shims with canonical globals content.
    """
    canonical = None
    for candidate in [project_root / "src/app/globals.css", project_root / "app/globals.css"]:
        text = read_text_if_exists(candidate)
        if text is not None:
            canonical = text
            break

    if canonical is None:
        return []

    created: List[str] = []
    for target in [project_root / "src/styles/globals.css", project_root / "styles/globals.css"]:
        if not target.exists():
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(
                "/* Auto-generated compatibility shim for '@/styles/globals.css' */\n" + canonical,
                encoding="utf-8",
            )
            created.append(str(target))

    return created


def write_meta(side_dir: Path, meta: Dict[str, Any], prompt: str, raw: str) -> None:
    (side_dir / "_meta.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")
    (side_dir / "_prompt.txt").write_text(prompt, encoding="utf-8")
    (side_dir / "_output_raw.json.txt").write_text(raw, encoding="utf-8")


def render_one_pair(
    pair: Dict[str, Any],
    templates_root: Path,
    out_root: Path,
    overwrite: bool,
) -> Dict[str, Any]:
    pair_id = str(pair.get("pair_id", ""))
    project = str(pair.get("project", ""))
    prompt = str(pair.get("prompt", ""))

    template_dir = find_template_project(templates_root, project)
    if not template_dir:
        raise FileNotFoundError(f"Template project '{project}' not found under {templates_root}")

    pair_dir = out_root / pair_id.replace("::", "--")
    pair_dir.mkdir(parents=True, exist_ok=True)

    summary: Dict[str, Any] = {
        "pair_id": pair_id,
        "brief_id": str(pair.get("brief_id", "")),
        "project": project,
        "template_dir": str(template_dir),
        "sides": {},
    }

    for side in ("A", "B"):
        side_dir = pair_dir / side
        raw = str(pair.get(f"output_{side}", ""))
        patches, err = parse_manifest_files(raw)

        # Always start from runnable template so user can preview UI even if patch is malformed.
        copy_template(template_dir, side_dir, overwrite=overwrite)

        applied = 0
        apply_error = ""
        if patches:
            try:
                applied = apply_patches(side_dir, patches)
            except Exception as exc:
                apply_error = f"apply_error: {exc}"

        compat_created = ensure_globals_css_compat(side_dir)

        meta = {
            "pair_id": pair_id,
            "side": side,
            "project": project,
            "template_dir": str(template_dir),
            "patch_count": len(patches),
            "patch_applied_count": applied,
            "parse_error": err,
            "apply_error": apply_error,
            "used_template_fallback": bool(err) or not patches,
            "compat_shims_created": compat_created,
            "is_runnable": (side_dir / "package.json").exists(),
        }

        write_meta(side_dir, meta, prompt, raw)
        summary["sides"][side] = meta

    (pair_dir / "_pair_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    return summary


def pick_pairs(pairs: List[Dict[str, Any]], pair_id: str, pair_index: int, all_pairs: bool, max_pairs: int) -> List[Dict[str, Any]]:
    if all_pairs:
        picked = list(pairs)
        if max_pairs > 0:
            picked = picked[:max_pairs]
        return picked

    if pair_id:
        out = [p for p in pairs if str(p.get("pair_id", "")) == pair_id]
        if not out:
            raise ValueError(f"pair-id not found: {pair_id}")
        return out

    if pair_index > 0:
        idx = pair_index - 1
        if idx < 0 or idx >= len(pairs):
            raise IndexError(f"pair-index out of range: {pair_index}")
        return [pairs[idx]]

    raise ValueError("Provide one of --all, --pair-id, or --pair-index")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--blind-pack", required=True)
    ap.add_argument("--templates-root", required=True)
    ap.add_argument("--out-root", required=True)
    ap.add_argument("--pair-id", default="")
    ap.add_argument("--pair-index", type=int, default=0, help="1-based")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--max-pairs", type=int, default=0)
    ap.add_argument("--overwrite", action="store_true")
    args = ap.parse_args()

    pack_path = Path(args.blind_pack).resolve()
    templates_root = Path(args.templates_root).resolve()
    out_root = Path(args.out_root).resolve()
    out_root.mkdir(parents=True, exist_ok=True)

    pairs = load_pack(pack_path)
    selected = pick_pairs(pairs, args.pair_id, args.pair_index, args.all, args.max_pairs)

    all_summaries: List[Dict[str, Any]] = []
    fallback_pairs = 0
    parse_error_sides = 0

    for i, pair in enumerate(selected, 1):
        summary = render_one_pair(pair, templates_root, out_root, overwrite=args.overwrite)
        all_summaries.append(summary)

        sides = summary.get("sides", {})
        side_a = sides.get("A", {})
        side_b = sides.get("B", {})
        if side_a.get("used_template_fallback") or side_b.get("used_template_fallback"):
            fallback_pairs += 1
        if side_a.get("parse_error"):
            parse_error_sides += 1
        if side_b.get("parse_error"):
            parse_error_sides += 1

        if i % 10 == 0 or i == len(selected):
            print(f"progress: rendered={i}/{len(selected)}")

    index_payload = {
        "blind_pack": str(pack_path),
        "out_root": str(out_root),
        "selected_count": len(selected),
        "fallback_pair_count": fallback_pairs,
        "parse_error_side_count": parse_error_sides,
        "pairs": all_summaries,
    }
    (out_root / "_render_index.json").write_text(json.dumps(index_payload, indent=2), encoding="utf-8")

    print("=== PAIR PREVIEW READY ===")
    print(f"pack:                  {pack_path}")
    print(f"out_root:              {out_root}")
    print(f"pairs_requested:       {len(selected)}")
    print(f"pairs_with_fallback:   {fallback_pairs}")
    print(f"sides_with_parse_err:  {parse_error_sides}")
    print(f"index:                 {out_root / '_render_index.json'}")


if __name__ == "__main__":
    main()
