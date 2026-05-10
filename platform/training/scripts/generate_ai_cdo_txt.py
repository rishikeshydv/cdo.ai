import argparse
import json
import os
import re
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import requests


OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
DEFAULT_MODEL = "openai/gpt-5.1"

ROLE_TAG = "<ROLE=EXECUTOR>"
BUCKET_TAG_TMPL = "<BUCKET={bucket}>"
UI_INTENT_TAG = "<UI_INTENT>"
CDO_BRIEF_TAG = "<CDO_BRIEF>"
SELECTED_STRATEGY_TAG = "<SELECTED_STRATEGY>"
TASK_TAG = "<TASK>"

SECTION_ORDER = [
    ROLE_TAG,
    "BUCKET",
    UI_INTENT_TAG,
    CDO_BRIEF_TAG,
    SELECTED_STRATEGY_TAG,
    TASK_TAG,
]

APP_DIRS = ["src/app", "app"]
COMPONENT_DIRS = ["src/components", "components"]
MAX_README_CHARS = 4000
MAX_FILE_CHARS = 2500
MAX_FILES_PER_PROJECT = 16


@dataclass
class ProjectContext:
    category: str
    bucket: str
    project_name: str
    project_path: Path
    app_dir: Optional[Path]
    component_dir: Optional[Path]
    package_json: str
    readme: str
    route_files: List[str]
    component_files: List[str]
    code_snippets: List[Tuple[str, str]]


def _bucket_from_category(category_name: str) -> str:
    # category-a -> A
    suffix = category_name.split("-")[-1].strip().upper()
    if suffix not in {"A", "B", "C"}:
        raise ValueError(f"Unsupported category naming: {category_name}")
    return suffix


def _safe_read(path: Path, max_chars: int) -> str:
    try:
        text = path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return ""
    text = text.strip()
    if len(text) > max_chars:
        return text[:max_chars] + "\n...<truncated>"
    return text


def _first_existing_dir(project_path: Path, candidates: List[str]) -> Optional[Path]:
    for rel in candidates:
        p = project_path / rel
        if p.is_dir():
            return p
    return None


def _collect_route_files(app_dir: Optional[Path], project_path: Path) -> List[str]:
    if not app_dir:
        return []
    routes = []
    for p in sorted(app_dir.rglob("page.tsx")):
        routes.append(p.relative_to(project_path).as_posix())
    return routes


def _collect_component_files(component_dir: Optional[Path], project_path: Path) -> List[str]:
    if not component_dir:
        return []
    files = []
    for p in sorted(component_dir.rglob("*.tsx")):
        files.append(p.relative_to(project_path).as_posix())
    return files


def _collect_candidate_snippet_files(
    project_path: Path,
    app_dir: Optional[Path],
    component_dir: Optional[Path],
) -> List[Path]:
    candidates: List[Path] = []

    for root_file in ["package.json", "README.md", "README.mdx"]:
        p = project_path / root_file
        if p.is_file():
            candidates.append(p)

    if app_dir:
        for rel in ["layout.tsx", "page.tsx", "globals.css"]:
            p = app_dir / rel
            if p.is_file():
                candidates.append(p)

        # Add a few more app route files to reflect multi-page context.
        for p in sorted(app_dir.rglob("page.tsx")):
            if p not in candidates:
                candidates.append(p)

    if component_dir:
        for p in sorted(component_dir.glob("*.tsx")):
            if p not in candidates:
                candidates.append(p)

    # Keep prompt bounded.
    return candidates[:MAX_FILES_PER_PROJECT]


def build_project_context(category_dir: Path, project_dir: Path) -> ProjectContext:
    bucket = _bucket_from_category(category_dir.name)
    app_dir = _first_existing_dir(project_dir, APP_DIRS)
    component_dir = _first_existing_dir(project_dir, COMPONENT_DIRS)

    package_json = _safe_read(project_dir / "package.json", MAX_FILE_CHARS)
    readme = _safe_read(project_dir / "README.md", MAX_README_CHARS)
    if not readme:
        readme = _safe_read(project_dir / "README.mdx", MAX_README_CHARS)

    route_files = _collect_route_files(app_dir, project_dir)
    component_files = _collect_component_files(component_dir, project_dir)

    code_snippets: List[Tuple[str, str]] = []
    for p in _collect_candidate_snippet_files(project_dir, app_dir, component_dir):
        snippet = _safe_read(p, MAX_FILE_CHARS)
        if snippet:
            code_snippets.append((p.relative_to(project_dir).as_posix(), snippet))

    return ProjectContext(
        category=category_dir.name,
        bucket=bucket,
        project_name=project_dir.name,
        project_path=project_dir,
        app_dir=app_dir,
        component_dir=component_dir,
        package_json=package_json,
        readme=readme,
        route_files=route_files,
        component_files=component_files,
        code_snippets=code_snippets,
    )


def _bucket_policy_hint(bucket: str) -> str:
    if bucket == "A":
        return (
            "Bucket A: conservative trust-first. Keep motion none/subtle, creative_license none/restricted, "
            "language precise, interaction restraint strict/moderate."
        )
    if bucket == "B":
        return (
            "Bucket B: balanced conversion. Motion subtle, creative_license restricted, "
            "language precise/confident, restraint moderate."
        )
    return (
        "Bucket C: expressive but still credible. Motion subtle/expressive with restraint, "
        "creative_license expressive, avoid gimmicks and unsafe claims."
    )


def make_messages(ctx: ProjectContext) -> List[Dict[str, str]]:
    system_prompt = (
        "You are generating training input files for an AI-CDO Step-5 Executor dataset.\n"
        "Return ONLY plaintext in this exact section order:\n"
        "<ROLE=EXECUTOR>\n"
        "<BUCKET=X>\n"
        "<UI_INTENT>\n"
        "{valid JSON}\n"
        "<CDO_BRIEF>\n"
        "{valid JSON}\n"
        "<SELECTED_STRATEGY>\n"
        "{valid JSON}\n"
        "<TASK>\n"
        "single paragraph task instruction\n\n"
        "Rules:\n"
        "- UI_INTENT must be valid JSON with keys: strategy_id, primary_focus, cta_policy{timing,intensity}, "
        "proof_policy, content_density, motion_policy, creative_license, language_style, interaction_restraint.\n"
        "- CDO_BRIEF must be valid JSON with keys: primary_intent, key_risks[], strategic_principles[], "
        "avoidances[], strategies[].\n"
        "- strategies must contain 2 or 3 strategy objects; each has: strategy_id, intent, hero_focus, "
        "information_order[], risk_controls[].\n"
        "- SELECTED_STRATEGY must be exactly one object copied from CDO_BRIEF.strategies.\n"
        "- Keep claims grounded to the repository context. No medical/legal/financial guarantees.\n"
        "- No markdown, no backticks, no explanations."
    )

    snippets_rendered = []
    for path, content in ctx.code_snippets:
        snippets_rendered.append(f"FILE: {path}\n{content}")

    user_prompt = (
        f"Project: {ctx.project_name}\n"
        f"Category: {ctx.category}\n"
        f"Required bucket: {ctx.bucket}\n"
        f"Policy hint: {_bucket_policy_hint(ctx.bucket)}\n"
        f"Detected app root: {ctx.app_dir.relative_to(ctx.project_path).as_posix() if ctx.app_dir else 'none'}\n"
        f"Detected component root: {ctx.component_dir.relative_to(ctx.project_path).as_posix() if ctx.component_dir else 'none'}\n"
        f"Route files: {json.dumps(ctx.route_files)}\n"
        f"Component files (sample): {json.dumps(ctx.component_files[:30])}\n\n"
        f"README:\n{ctx.readme or '<none>'}\n\n"
        f"package.json:\n{ctx.package_json or '<none>'}\n\n"
        "Key code context:\n"
        + "\n\n".join(snippets_rendered)
    )

    return [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]


def call_openrouter(api_key: str, model: str, messages: List[Dict[str, str]]) -> str:
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": model,
        "messages": messages,
        "temperature": 0.2,
        "max_tokens": 4000,
    }
    resp = requests.post(OPENROUTER_URL, headers=headers, json=payload, timeout=180)
    resp.raise_for_status()
    data = resp.json()
    try:
        return data["choices"][0]["message"]["content"].strip()
    except Exception as exc:
        raise RuntimeError(f"Unexpected OpenRouter response shape: {data}") from exc


def _extract_json_block(text: str, start_tag: str, end_tag: Optional[str]) -> str:
    start_idx = text.find(start_tag)
    if start_idx < 0:
        return ""
    start_idx += len(start_tag)
    if end_tag:
        end_idx = text.find(end_tag, start_idx)
        if end_idx < 0:
            return ""
        chunk = text[start_idx:end_idx]
    else:
        chunk = text[start_idx:]
    return chunk.strip()


def validate_ai_cdo_text(text: str, expected_bucket: str) -> Tuple[bool, str]:
    if ROLE_TAG not in text:
        return False, "missing <ROLE=EXECUTOR>"
    if BUCKET_TAG_TMPL.format(bucket=expected_bucket) not in text:
        return False, f"missing or wrong <BUCKET={expected_bucket}>"
    for tag in [UI_INTENT_TAG, CDO_BRIEF_TAG, SELECTED_STRATEGY_TAG, TASK_TAG]:
        if tag not in text:
            return False, f"missing {tag}"

    ui_text = _extract_json_block(text, UI_INTENT_TAG, CDO_BRIEF_TAG)
    brief_text = _extract_json_block(text, CDO_BRIEF_TAG, SELECTED_STRATEGY_TAG)
    selected_text = _extract_json_block(text, SELECTED_STRATEGY_TAG, TASK_TAG)
    task_text = _extract_json_block(text, TASK_TAG, None)

    if not task_text:
        return False, "empty <TASK> section"

    try:
        ui_obj = json.loads(ui_text)
    except Exception as exc:
        return False, f"invalid UI_INTENT JSON: {exc}"
    try:
        brief_obj = json.loads(brief_text)
    except Exception as exc:
        return False, f"invalid CDO_BRIEF JSON: {exc}"
    try:
        selected_obj = json.loads(selected_text)
    except Exception as exc:
        return False, f"invalid SELECTED_STRATEGY JSON: {exc}"

    required_ui = {
        "strategy_id",
        "primary_focus",
        "cta_policy",
        "proof_policy",
        "content_density",
        "motion_policy",
        "creative_license",
        "language_style",
        "interaction_restraint",
    }
    if not required_ui.issubset(set(ui_obj.keys())):
        return False, "UI_INTENT missing required keys"

    if not isinstance(brief_obj.get("strategies"), list) or len(brief_obj["strategies"]) < 2:
        return False, "CDO_BRIEF.strategies must contain at least 2 entries"

    strategy_ids = {
        s.get("strategy_id")
        for s in brief_obj["strategies"]
        if isinstance(s, dict) and s.get("strategy_id")
    }
    if selected_obj.get("strategy_id") not in strategy_ids:
        return False, "SELECTED_STRATEGY.strategy_id not present in CDO_BRIEF.strategies"
    if ui_obj.get("strategy_id") != selected_obj.get("strategy_id"):
        return False, "UI_INTENT.strategy_id must match SELECTED_STRATEGY.strategy_id"

    return True, "ok"


def generate_ai_cdo_for_project(
    ctx: ProjectContext,
    api_key: str,
    model: str,
    retries: int = 2,
) -> str:
    messages = make_messages(ctx)
    last_err = "unknown"
    for attempt in range(1, retries + 1):
        text = call_openrouter(api_key=api_key, model=model, messages=messages)
        ok, reason = validate_ai_cdo_text(text, expected_bucket=ctx.bucket)
        if ok:
            return text.strip() + "\n"
        last_err = reason
        # Retry with explicit correction instruction.
        messages = messages + [
            {
                "role": "assistant",
                "content": text,
            },
            {
                "role": "user",
                "content": (
                    f"The previous output failed validation: {reason}. "
                    f"Return corrected output only, keep bucket {ctx.bucket}, and keep the same section order."
                ),
            },
        ]
    raise RuntimeError(f"Failed validation after retries: {last_err}")


def iter_projects(templates_root: Path, categories: List[str]) -> List[Tuple[Path, Path]]:
    pairs: List[Tuple[Path, Path]] = []
    for cat_name in categories:
        cat_dir = templates_root / cat_name
        if not cat_dir.is_dir():
            continue
        for project_dir in sorted(cat_dir.iterdir()):
            if project_dir.is_dir():
                pairs.append((cat_dir, project_dir))
    return pairs


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--templates-root",
        default=str((Path(__file__).resolve().parent / "../../../datasets/templates").resolve()),
    )
    parser.add_argument(
        "--categories",
        nargs="+",
        default=["category-a", "category-b", "category-c"],
    )
    parser.add_argument("--model", default=os.getenv("OPENROUTER_CHAT_MODEL", DEFAULT_MODEL))
    parser.add_argument("--overwrite", action="store_true")
    parser.add_argument("--max-projects", type=int, default=0)
    parser.add_argument("--sleep-seconds", type=float, default=0.4)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    api_key = os.getenv("OPENROUTER_API_KEY", "").strip()
    if not api_key:
        raise RuntimeError("OPENROUTER_API_KEY is required.")

    templates_root = Path(args.templates_root).resolve()
    project_pairs = iter_projects(templates_root, args.categories)
    if args.max_projects > 0:
        project_pairs = project_pairs[: args.max_projects]

    generated = 0
    skipped_existing = 0
    failed = 0

    print("=== AI-CDO Generation Start ===")
    print(f"Templates root: {templates_root}")
    print(f"Projects found: {len(project_pairs)}")
    print(f"Model: {args.model}")
    print(f"Overwrite: {args.overwrite}")

    for idx, (cat_dir, project_dir) in enumerate(project_pairs, start=1):
        out_path = project_dir / "ai-cdo.txt"
        if out_path.exists() and not args.overwrite:
            skipped_existing += 1
            print(f"[{idx}/{len(project_pairs)}] SKIP existing: {project_dir.name}")
            continue

        try:
            ctx = build_project_context(cat_dir, project_dir)
            text = generate_ai_cdo_for_project(ctx=ctx, api_key=api_key, model=args.model)
            if args.dry_run:
                print(f"[{idx}/{len(project_pairs)}] DRY-RUN generated: {project_dir.name}")
            else:
                out_path.write_text(text, encoding="utf-8")
                print(f"[{idx}/{len(project_pairs)}] GENERATED: {project_dir.name}")
            generated += 1
        except Exception as exc:
            failed += 1
            print(f"[{idx}/{len(project_pairs)}] FAILED: {project_dir.name} :: {exc}")
        time.sleep(args.sleep_seconds)

    print("\n=== AI-CDO Generation Summary ===")
    print(f"Generated: {generated}")
    print(f"Skipped existing: {skipped_existing}")
    print(f"Failed: {failed}")


if __name__ == "__main__":
    main()
