import json
import argparse
from pathlib import Path
from typing import Any, Dict, List, Tuple
from collections import defaultdict


SYSTEM_PROMPT = """
You are the Step-5 Executor in a multi-stage AI-CDO system.

Input you receive:
- UI Intent JSON
- Full CDO Brief JSON
- Selected Strategy object

Your output MUST be a JSON manifest only:

{
  "files": [{"path": "...", "content": "..."}],
  "instructions": "npm install && npm run dev"
}

Rules:
- Obey UI Intent strictly
- Follow selected strategy exactly
- Generate modular Next.js App Router code (TypeScript + Tailwind)
- No explanations
- No markdown
- Output valid JSON only
""".strip()

APP_ROOT_SETS = [
    ["app/page.tsx", "app/layout.tsx", "app/globals.css"],
    ["src/app/page.tsx", "src/app/layout.tsx", "src/app/globals.css"],
]

COMPONENT_ROOTS = [
    "components/",
    "src/components/",
]

REQUIRED_ROOT_FILES = [
    "package.json",
]



def clean_text(s: str) -> str:
    if not s:
        return ""
    return s.replace("\ufeff", "").replace("\x00", "").strip()


def parse_json_relaxed(line: str) -> Dict[str, Any]:
    return json.loads(line)


def validate_manifest(text: str) -> Tuple[Dict[str, Any], List[str]]:
    errors: List[str] = []

    try:
        manifest = json.loads(text)
    except Exception as e:
        return {}, [f"manifest_not_json: {e}"]

    if not isinstance(manifest, dict):
        return {}, ["manifest_not_object"]

    files = manifest.get("files")
    if not isinstance(files, list) or not files:
        errors.append("manifest_missing_files")

    instructions = manifest.get("instructions")
    if not isinstance(instructions, str) or not instructions.strip():
        errors.append("manifest_missing_instructions")

    paths = []
    file_map = {}

    for f in files:
        if not isinstance(f, dict):
            continue
        p = f.get("path")
        c = f.get("content")
        if isinstance(p, str) and isinstance(c, str):
            norm = p.replace("\\", "/")
            paths.append(norm)
            file_map[norm] = c

    # ---- root runtime files ----
    for req in REQUIRED_ROOT_FILES:
        if req not in paths:
            errors.append(f"missing_required_file:{req}")

    # ---- app router detection ----
    app_root = None
    for candidate in APP_ROOT_SETS:
        if all(p in paths for p in candidate):
            app_root = candidate[0].rsplit("/", 1)[0]  # app or src/app
            break


    if not app_root:
        errors.append("missing_app_router_files")
        return manifest, errors

    page_path = f"{app_root}/page.tsx"

    # ---- component detection ----
    component_files = [
        p for p in paths
        if any(p.startswith(root) for root in COMPONENT_ROOTS) and p.endswith(".tsx")
    ]

    if len(component_files) < 2:
        errors.append("insufficient_components")

    # ---- component usage in page.tsx ----
    page_code = file_map.get(page_path, "")
    used = False
    for comp in component_files:
        name = comp.split("/")[-1].replace(".tsx", "")
        if name and name in page_code:
            used = True
            break

    if not used:
        errors.append("components_not_used_in_page")

    return manifest, errors


def convert_record(ex: Dict[str, Any]) -> Tuple[Dict[str, Any], List[str]]:
    errors: List[str] = []

    if "input" not in ex:
        errors.append("missing_input")
    if "output" not in ex:
        errors.append("missing_output")

    user_content = clean_text(ex.get("input", ""))
    assistant_content = clean_text(ex.get("output", ""))

    if not user_content:
        errors.append("empty_input")
    if not assistant_content:
        errors.append("empty_output")

    _, manifest_errors = validate_manifest(assistant_content)
    errors.extend(manifest_errors)

    if errors:
        return {}, errors

    record = {
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_content},
            {"role": "assistant", "content": assistant_content},
        ]
    }
    return record, []


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True)
    ap.add_argument("--output", required=True)
    ap.add_argument("--report", default="")
    ap.add_argument("--max", type=int, default=0)
    args = ap.parse_args()

    in_path = Path(args.input).resolve()
    out_path = Path(args.output).resolve()
    out_path.parent.mkdir(parents=True, exist_ok=True)

    skip_reasons = defaultdict(int)
    skip_examples = []

    ok = 0
    skipped = 0

    with in_path.open("r", encoding="utf-8") as f_in, out_path.open("w", encoding="utf-8") as f_out:
        for idx, line in enumerate(f_in, start=1):
            if args.max and ok + skipped >= args.max:
                break

            line = line.strip()
            if not line:
                continue

            try:
                ex = parse_json_relaxed(line)
                record, errors = convert_record(ex)

                if errors:
                    skipped += 1
                    skip_reasons[errors[0]] += 1
                    if len(skip_examples) < 200:
                        skip_examples.append({
                            "line": idx,
                            "id": ex.get("id"),
                            "project": ex.get("project"),
                            "bucket": ex.get("bucket"),
                            "errors": errors[:8],
                        })
                    continue

                f_out.write(json.dumps(record, ensure_ascii=False) + "\n")
                ok += 1

            except Exception as e:
                skipped += 1
                skip_reasons["parse_error"] += 1
                if len(skip_examples) < 200:
                    skip_examples.append({
                        "line": idx,
                        "raw": line[:200],
                        "errors": [str(e)],
                    })

    print("\n=== PHASE 2 SUMMARY ===")
    print(f"Input:  {in_path}")
    print(f"Output: {out_path}")
    print(f"OK:     {ok}")
    print(f"SKIP:   {skipped}")

    print("\n=== TOP SKIP REASONS ===")
    for k, v in sorted(skip_reasons.items(), key=lambda x: x[1], reverse=True)[:20]:
        print(f"{v:>6}  {k}")

    if args.report:
        rep_path = Path(args.report).resolve()
        rep_path.parent.mkdir(parents=True, exist_ok=True)
        rep_path.write_text(
            json.dumps({
                "ok": ok,
                "skipped": skipped,
                "skip_reasons": dict(skip_reasons),
                "examples": skip_examples,
            }, indent=2),
            encoding="utf-8"
        )
        print(f"\nReport written to: {rep_path}")


if __name__ == "__main__":
    main()


#run this code using:
# python3 convert_to_openai.py --input ../data/sft_data.jsonl --output ../data/openai_data.jsonl --report ../data/convert_report.json --max 0