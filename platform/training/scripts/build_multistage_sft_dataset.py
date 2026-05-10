import argparse
import json
import random
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Tuple


DATASET_CATEGORIES = ["category-a", "category-b", "category-c"]
APP_DIRS = ["src/app", "app"]
COMPONENT_DIRS = ["src/components", "components"]
CANONICAL_APP_DIR = "src/app"
CANONICAL_COMPONENT_DIR = "src/components"

REQUIRED_APP_FILES = ["page.tsx", "layout.tsx", "globals.css"]
OPTIONAL_RUNTIME_FILES = ["package.json"]

STAGE_FULL = "sft_full_aug"
STAGE_1 = "sft_stage1_short"
STAGE_2 = "sft_stage2_filewise"
STAGE_EVAL = "eval_prod_like"

FULL_SYSTEM_PROMPT = (
    "You are the Step-5 Executor in a multi-stage AI-CDO system. "
    "Return only valid JSON manifest with files[] and instructions. "
    "Obey UI intent, selected strategy, and risk controls exactly."
)

STAGE1_SYSTEM_PROMPT = (
    "You are preparing a short execution plan before code generation. "
    "Return valid JSON only with: plan[], manifest_skeleton{files[],instructions}, "
    "policy{bucket,cta_policy,motion_policy,creative_license,interaction_restraint}, selected_strategy_id."
)

STAGE2_FILE_SYSTEM_PROMPT = (
    "You are a file-level Next.js executor. Return only valid JSON with {path, content}. "
    "Generate only the requested file and keep consistency with the provided intent and strategy."
)

STAGE2_REPAIR_SYSTEM_PROMPT = (
    "You are a file repair executor. You receive one broken target file and must return corrected code. "
    "Return only valid JSON with {path, content}."
)

PROMPT_VARIANTS = ["original", "compressed", "paraphrase", "noisy", "ambiguous"]

POLICY_PRESETS: Dict[str, Dict[str, Any]] = {
    "A": {
        "cta_policy": {"timing": "delayed", "intensity": "low"},
        "proof_policy": "heavy",
        "content_density": "medium",
        "motion_policy": "none",
        "creative_license": "none",
        "language_style": "precise",
        "interaction_restraint": "strict",
    },
    "B": {
        "cta_policy": {"timing": "balanced", "intensity": "medium"},
        "proof_policy": "balanced",
        "content_density": "medium",
        "motion_policy": "subtle",
        "creative_license": "restricted",
        "language_style": "precise_confident",
        "interaction_restraint": "moderate",
    },
    "C": {
        "cta_policy": {"timing": "early", "intensity": "high"},
        "proof_policy": "balanced",
        "content_density": "high",
        "motion_policy": "expressive_with_restraint",
        "creative_license": "expressive",
        "language_style": "bold_clear",
        "interaction_restraint": "moderate",
    },
}


@dataclass
class ProjectSample:
    category: str
    bucket: str
    project: str
    ai_cdo: str
    files: List[Dict[str, str]]


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore").rstrip()


def dump_json(obj: Any) -> str:
    return json.dumps(obj, ensure_ascii=False)


def find_section_bounds(text: str, start_tag: str, end_tag: Optional[str]) -> Optional[Tuple[int, int]]:
    start = text.find(start_tag)
    if start < 0:
        return None
    start_content = start + len(start_tag)
    if end_tag is None:
        return start_content, len(text)
    end = text.find(end_tag, start_content)
    if end < 0:
        return None
    return start_content, end


def extract_section_text(text: str, start_tag: str, end_tag: Optional[str]) -> str:
    bounds = find_section_bounds(text, start_tag, end_tag)
    if not bounds:
        return ""
    a, b = bounds
    return text[a:b].strip()


def replace_section_text(text: str, start_tag: str, end_tag: Optional[str], replacement: str) -> str:
    bounds = find_section_bounds(text, start_tag, end_tag)
    if not bounds:
        if start_tag == "<TASK>":
            return text.rstrip() + "\n<TASK>\n" + replacement.strip() + "\n"
        return text
    a, b = bounds
    return text[:a] + "\n" + replacement.strip() + "\n" + text[b:]


def extract_task(ai_cdo: str) -> str:
    return extract_section_text(ai_cdo, "<TASK>", None)


def replace_task(ai_cdo: str, task_text: str) -> str:
    return replace_section_text(ai_cdo, "<TASK>", None, task_text)


def extract_ui_intent(ai_cdo: str) -> Dict[str, Any]:
    raw = extract_section_text(ai_cdo, "<UI_INTENT>", "<CDO_BRIEF>")
    if not raw:
        return {}
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return {}


def replace_ui_intent(ai_cdo: str, ui_intent: Dict[str, Any]) -> str:
    return replace_section_text(ai_cdo, "<UI_INTENT>", "<CDO_BRIEF>", dump_json(ui_intent))


def extract_selected_strategy_id(ai_cdo: str) -> str:
    raw = extract_section_text(ai_cdo, "<SELECTED_STRATEGY>", "<TASK>")
    if not raw:
        return ""
    try:
        obj = json.loads(raw)
    except json.JSONDecodeError:
        return ""
    sid = obj.get("strategy_id")
    return sid if isinstance(sid, str) else ""


def compress_text(text: str, words: int) -> str:
    tokens = re.findall(r"\S+", text)
    if len(tokens) <= words:
        return text.strip()
    return " ".join(tokens[:words]).strip() + " ..."


def noisy_text(text: str) -> str:
    compressed = compress_text(text, 55).lower()
    compressed = compressed.replace(" and ", " & ")
    compressed = compressed.replace(" with ", " w/ ")
    compressed = re.sub(r"[^a-z0-9\s_\-#/&]", "", compressed)
    compressed = re.sub(r"\s+", " ", compressed).strip()
    return compressed


def apply_prompt_variant(ai_cdo: str, variant: str) -> str:
    task = extract_task(ai_cdo)
    if not task:
        return ai_cdo

    if variant == "original":
        new_task = task
    elif variant == "compressed":
        new_task = compress_text(task, 45)
    elif variant == "paraphrase":
        new_task = (
            "Build the same product outcome under the same UI intent and selected strategy. "
            + compress_text(task, 60)
        )
    elif variant == "noisy":
        new_task = noisy_text(task)
    elif variant == "ambiguous":
        new_task = (
            "Create a premium and trustworthy implementation for this product request. "
            "Keep all policy and strategy constraints from the sections above."
        )
    else:
        new_task = task

    return replace_task(ai_cdo, new_task)


def apply_policy_variant(ai_cdo: str, target_bucket: str) -> str:
    updated = re.sub(r"<BUCKET=[ABC]>", f"<BUCKET={target_bucket}>", ai_cdo, count=1)

    ui = extract_ui_intent(updated)
    if not ui:
        return updated

    preset = POLICY_PRESETS[target_bucket]
    for k, v in preset.items():
        ui[k] = v

    return replace_ui_intent(updated, ui)


def pick_app_dir(project_path: Path) -> Optional[Path]:
    candidates: List[Tuple[int, Path]] = []
    for rel in APP_DIRS:
        root = project_path / rel
        if not root.is_dir():
            continue
        score = 0
        for fname in REQUIRED_APP_FILES:
            if (root / fname).is_file():
                score += 1
        candidates.append((score, root))

    if not candidates:
        return None

    candidates.sort(key=lambda x: x[0], reverse=True)
    best_score = candidates[0][0]
    best_paths = [p for s, p in candidates if s == best_score]

    for preferred in APP_DIRS:
        preferred_path = project_path / preferred
        if preferred_path in best_paths:
            return preferred_path

    return best_paths[0]


def pick_component_dir(project_path: Path) -> Optional[Path]:
    candidates: List[Tuple[int, Path]] = []
    for rel in COMPONENT_DIRS:
        root = project_path / rel
        if not root.is_dir():
            continue
        count = len([p for p in root.rglob("*.tsx") if p.is_file()])
        candidates.append((count, root))

    if not candidates:
        return None

    candidates.sort(key=lambda x: x[0], reverse=True)
    best_count = candidates[0][0]
    best_paths = [p for c, p in candidates if c == best_count]

    for preferred in COMPONENT_DIRS:
        preferred_path = project_path / preferred
        if preferred_path in best_paths:
            return preferred_path

    return best_paths[0]


def canonical_path_for_app(app_root: Path, p: Path) -> str:
    rel = p.relative_to(app_root).as_posix()
    return f"{CANONICAL_APP_DIR}/{rel}"


def canonical_path_for_component(component_root: Path, p: Path) -> str:
    rel = p.relative_to(component_root).as_posix()
    return f"{CANONICAL_COMPONENT_DIR}/{rel}"


def collect_files(project_path: Path) -> List[Dict[str, str]]:
    file_map: Dict[str, str] = {}

    for root_file in OPTIONAL_RUNTIME_FILES:
        p = project_path / root_file
        if p.is_file():
            file_map[root_file] = read_text(p)

    app_root = pick_app_dir(project_path)
    if not app_root:
        return []

    for required in REQUIRED_APP_FILES:
        p = app_root / required
        if p.is_file():
            file_map[canonical_path_for_app(app_root, p)] = read_text(p)

    if f"{CANONICAL_APP_DIR}/page.tsx" not in file_map:
        return []

    app_patterns = [
        "**/page.tsx",
        "**/layout.tsx",
        "**/loading.tsx",
        "**/error.tsx",
        "**/not-found.tsx",
        "**/template.tsx",
        "**/*.css",
    ]
    for pattern in app_patterns:
        for p in sorted(app_root.glob(pattern)):
            if not p.is_file():
                continue
            key = canonical_path_for_app(app_root, p)
            if key not in file_map:
                file_map[key] = read_text(p)

    component_root = pick_component_dir(project_path)
    if component_root:
        for p in sorted(component_root.rglob("*.tsx")):
            if not p.is_file():
                continue
            key = canonical_path_for_component(component_root, p)
            file_map[key] = read_text(p)

    files = [{"path": k, "content": v} for k, v in sorted(file_map.items())]
    return files


def detect_file_kind(path: str) -> str:
    if path == "package.json":
        return "runtime"
    if path.endswith("/page.tsx"):
        return "app_page"
    if path.endswith("/layout.tsx"):
        return "app_layout"
    if path.endswith(".css"):
        return "style"
    if path.startswith("src/components/"):
        return "component"
    return "other"


def build_manifest(files: List[Dict[str, str]]) -> Dict[str, Any]:
    return {
        "files": files,
        "instructions": "npm install && npm run dev",
    }


def build_stage1_output(
    files: List[Dict[str, str]],
    bucket: str,
    ui_intent: Dict[str, Any],
    selected_strategy_id: str,
) -> Dict[str, Any]:
    skeleton_files = []
    for f in files:
        skeleton_files.append({
            "path": f["path"],
            "kind": detect_file_kind(f["path"]),
        })

    return {
        "plan": [
            "Lock policy and strategy constraints before coding.",
            "Generate foundational app files and shared styles first.",
            "Generate page and components with restrained interaction patterns.",
            "Run structural and policy validation before shipping.",
        ],
        "manifest_skeleton": {
            "files": skeleton_files,
            "instructions": "npm install && npm run dev",
        },
        "policy": {
            "bucket": bucket,
            "cta_policy": ui_intent.get("cta_policy", {}),
            "motion_policy": ui_intent.get("motion_policy", ""),
            "creative_license": ui_intent.get("creative_license", ""),
            "interaction_restraint": ui_intent.get("interaction_restraint", ""),
        },
        "selected_strategy_id": selected_strategy_id,
    }


def build_filewise_output(path: str, content: str) -> Dict[str, str]:
    return {"path": path, "content": content}


def build_file_generation_input(base_input: str, target_path: str, all_paths: Sequence[str]) -> str:
    context_paths = list(all_paths[:25])
    instruction = (
        "\n<EXECUTION_MODE=FILE_ONLY>\n"
        f"<TARGET_FILE>{target_path}</TARGET_FILE>\n"
        f"<CONTEXT_FILE_LIST>{dump_json(context_paths)}</CONTEXT_FILE_LIST>\n"
        "Return JSON only: {\"path\":\"...\",\"content\":\"...\"}. Generate only the target file."
    )
    return base_input.rstrip() + "\n" + instruction


def make_corrupted_content(content: str, seed: int) -> Tuple[str, List[str]]:
    rng = random.Random(seed)
    lines = content.splitlines()
    ops: List[str] = []

    import_indexes = [i for i, line in enumerate(lines) if line.strip().startswith("import ")]
    if import_indexes:
        idx = import_indexes[0]
        lines.pop(idx)
        ops.append("missing_import")

    joined = "\n".join(lines)
    if "className=" in joined:
        joined = joined.replace("className=", "class=", 1)
        ops.append("jsx_attr_regression")

    lines = joined.splitlines()
    close_indexes = [
        i for i, line in enumerate(lines)
        if line.strip() in {"}", "};", "</section>", "</div>", ")", ");"}
    ]
    if close_indexes:
        idx = close_indexes[-1]
        lines.pop(idx)
        ops.append("missing_closer")

    broken = "\n".join(lines)

    if not ops:
        if len(broken) > 40:
            cut = rng.randint(20, min(80, len(broken) - 1))
            broken = broken[:-cut]
        else:
            broken = broken + "\nconst __broken ="
        ops.append("truncated_tail")

    return broken, ops


def build_repair_input(base_input: str, target_path: str, broken: str, issues: List[str]) -> str:
    instruction = (
        "\n<EXECUTION_MODE=REPAIR_FILE>\n"
        f"<TARGET_FILE>{target_path}</TARGET_FILE>\n"
        f"<KNOWN_ISSUES>{dump_json(issues)}</KNOWN_ISSUES>\n"
        "<BROKEN_FILE>\n"
        f"{broken}\n"
        "</BROKEN_FILE>\n"
        "Return JSON only: {\"path\":\"...\",\"content\":\"...\"}."
    )
    return base_input.rstrip() + "\n" + instruction


def split_by_project(records: List[Dict[str, Any]], val_ratio: float, seed: int) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    projects = sorted({r["project"] for r in records})
    rng = random.Random(seed)
    rng.shuffle(projects)

    if not projects:
        return [], []

    val_n = max(1, int(len(projects) * val_ratio)) if len(projects) > 1 else 0
    val_projects = set(projects[:val_n])

    train = [r for r in records if r["project"] not in val_projects]
    val = [r for r in records if r["project"] in val_projects]
    return train, val


def to_openai_records(records: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    out = []
    for r in records:
        if "input" not in r or "output" not in r:
            continue
        out.append(
            {
                "messages": [
                    {"role": "system", "content": r.get("system", FULL_SYSTEM_PROMPT)},
                    {"role": "user", "content": r["input"]},
                    {"role": "assistant", "content": r["output"]},
                ]
            }
        )
    return out


def write_jsonl(path: Path, rows: Sequence[Dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")


def gather_projects(templates_root: Path) -> List[ProjectSample]:
    projects: List[ProjectSample] = []

    for category in DATASET_CATEGORIES:
        cat_dir = templates_root / category
        if not cat_dir.is_dir():
            continue

        bucket = category[-1].upper()

        for project_dir in sorted(cat_dir.iterdir()):
            if not project_dir.is_dir():
                continue

            ai_cdo_path = project_dir / "ai-cdo.txt"
            if not ai_cdo_path.is_file():
                continue

            ai_cdo = read_text(ai_cdo_path).strip()
            if not ai_cdo:
                continue

            files = collect_files(project_dir)
            if not files:
                continue

            projects.append(
                ProjectSample(
                    category=category,
                    bucket=bucket,
                    project=project_dir.name,
                    ai_cdo=ai_cdo,
                    files=files,
                )
            )

    return projects


def build_records_for_project(
    sample: ProjectSample,
    max_components_per_project: int,
    repair_component_count: int,
) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]], List[Dict[str, Any]], List[Dict[str, Any]]]:
    full_records: List[Dict[str, Any]] = []
    stage1_records: List[Dict[str, Any]] = []
    stage2_records: List[Dict[str, Any]] = []
    dpo_seed_records: List[Dict[str, Any]] = []

    base_manifest = build_manifest(sample.files)
    full_output = dump_json(base_manifest)

    # full-build samples
    for variant in ["original", "compressed"]:
        v_input = apply_prompt_variant(sample.ai_cdo, variant)
        full_records.append(
            {
                "id": f"{sample.category}-{sample.project}::full::{variant}",
                "project": sample.project,
                "bucket": sample.bucket,
                "stage": STAGE_FULL,
                "kind": "full_build",
                "variant": variant,
                "system": FULL_SYSTEM_PROMPT,
                "input": v_input,
                "output": full_output,
            }
        )

    # stage-1 short plan and policy variants
    for policy_bucket in ["A", "B", "C"]:
        policy_input = apply_policy_variant(sample.ai_cdo, policy_bucket)
        ui_intent = extract_ui_intent(policy_input)
        strategy_id = extract_selected_strategy_id(policy_input)
        s1_output = dump_json(build_stage1_output(sample.files, policy_bucket, ui_intent, strategy_id))

        for variant in PROMPT_VARIANTS:
            v_input = apply_prompt_variant(policy_input, variant)
            stage1_records.append(
                {
                    "id": f"{sample.category}-{sample.project}::s1::{policy_bucket}::{variant}",
                    "project": sample.project,
                    "bucket": policy_bucket,
                    "source_bucket": sample.bucket,
                    "stage": STAGE_1,
                    "kind": f"policy_variant_{policy_bucket}",
                    "variant": variant,
                    "system": STAGE1_SYSTEM_PROMPT,
                    "input": v_input,
                    "output": s1_output,
                }
            )

    # stage-2 file-wise generation and repair
    all_paths = [f["path"] for f in sample.files]
    page_file = next((f for f in sample.files if f["path"] == "src/app/page.tsx"), None)
    component_files = [f for f in sample.files if f["path"].startswith("src/components/") and f["path"].endswith(".tsx")]
    component_files = component_files[:max_components_per_project]

    if page_file:
        for variant in ["original", "compressed", "paraphrase"]:
            v_input = apply_prompt_variant(sample.ai_cdo, variant)
            user_input = build_file_generation_input(v_input, page_file["path"], all_paths)
            stage2_records.append(
                {
                    "id": f"{sample.category}-{sample.project}::s2::page::{variant}",
                    "project": sample.project,
                    "bucket": sample.bucket,
                    "stage": STAGE_2,
                    "kind": "page_only",
                    "variant": variant,
                    "target_path": page_file["path"],
                    "system": STAGE2_FILE_SYSTEM_PROMPT,
                    "input": user_input,
                    "output": dump_json(build_filewise_output(page_file["path"], page_file["content"])),
                }
            )

    for idx, comp in enumerate(component_files):
        variant = "compressed" if idx < 2 else "original"
        v_input = apply_prompt_variant(sample.ai_cdo, variant)
        user_input = build_file_generation_input(v_input, comp["path"], all_paths)
        stage2_records.append(
            {
                "id": f"{sample.category}-{sample.project}::s2::component::{idx}",
                "project": sample.project,
                "bucket": sample.bucket,
                "stage": STAGE_2,
                "kind": "component_only",
                "variant": variant,
                "target_path": comp["path"],
                "system": STAGE2_FILE_SYSTEM_PROMPT,
                "input": user_input,
                "output": dump_json(build_filewise_output(comp["path"], comp["content"])),
            }
        )

    repair_targets: List[Dict[str, str]] = []
    if page_file:
        repair_targets.append(page_file)
    repair_targets.extend(component_files[:repair_component_count])

    for idx, target in enumerate(repair_targets):
        broken, issues = make_corrupted_content(
            target["content"],
            seed=abs(hash(f"{sample.project}:{target['path']}")) % (2**31),
        )
        user_input = build_repair_input(sample.ai_cdo, target["path"], broken, issues)

        stage2_records.append(
            {
                "id": f"{sample.category}-{sample.project}::s2::repair::{idx}",
                "project": sample.project,
                "bucket": sample.bucket,
                "stage": STAGE_2,
                "kind": "repair",
                "variant": "repair",
                "target_path": target["path"],
                "system": STAGE2_REPAIR_SYSTEM_PROMPT,
                "input": user_input,
                "output": dump_json(build_filewise_output(target["path"], target["content"])),
            }
        )

        dpo_seed_records.append(
            {
                "id": f"{sample.category}-{sample.project}::dpo_seed::{idx}",
                "project": sample.project,
                "bucket": sample.bucket,
                "stage": "dpo_seed",
                "kind": "repair_preference",
                "system": STAGE2_REPAIR_SYSTEM_PROMPT,
                "prompt": user_input,
                "chosen": dump_json(build_filewise_output(target["path"], target["content"])),
                "rejected": dump_json(build_filewise_output(target["path"], broken)),
                "issues": issues,
            }
        )

    return full_records, stage1_records, stage2_records, dpo_seed_records


def build_eval_records(sample: ProjectSample) -> List[Dict[str, Any]]:
    manifest = dump_json(build_manifest(sample.files))
    out: List[Dict[str, Any]] = []

    for variant in PROMPT_VARIANTS:
        v_input = apply_prompt_variant(sample.ai_cdo, variant)
        out.append(
            {
                "id": f"{sample.category}-{sample.project}::eval::{variant}",
                "project": sample.project,
                "bucket": sample.bucket,
                "stage": STAGE_EVAL,
                "variant": variant,
                "system": FULL_SYSTEM_PROMPT,
                "input": v_input,
                "expected_output": manifest,
                "checks": [
                    "app_root_structure",
                    "component_modularity",
                    "cta_policy_alignment",
                    "motion_policy_alignment",
                    "creative_license_alignment",
                ],
            }
        )

    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--templates-root",
        default=str((Path(__file__).resolve().parent / "../../../datasets/templates").resolve()),
    )
    ap.add_argument(
        "--out-dir",
        default=str((Path(__file__).resolve().parent / "../data/augmented").resolve()),
    )
    ap.add_argument("--seed", type=int, default=1337)
    ap.add_argument("--val-ratio", type=float, default=0.1)
    ap.add_argument("--holdout-ratio", type=float, default=0.2)
    ap.add_argument("--max-components-per-project", type=int, default=8)
    ap.add_argument("--repair-component-count", type=int, default=2)
    args = ap.parse_args()

    templates_root = Path(args.templates_root).resolve()
    out_dir = Path(args.out_dir).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    projects = gather_projects(templates_root)
    if not projects:
        raise RuntimeError(f"No projects found in {templates_root}")

    rng = random.Random(args.seed)
    project_names = sorted({p.project for p in projects})
    rng.shuffle(project_names)
    holdout_n = max(1, int(len(project_names) * args.holdout_ratio)) if len(project_names) > 1 else 0
    holdout_projects = set(project_names[:holdout_n])

    full_records: List[Dict[str, Any]] = []
    stage1_records: List[Dict[str, Any]] = []
    stage2_records: List[Dict[str, Any]] = []
    eval_records: List[Dict[str, Any]] = []
    dpo_seed_records: List[Dict[str, Any]] = []

    for sample in projects:
        if sample.project in holdout_projects:
            eval_records.extend(build_eval_records(sample))
            continue

        full_r, s1_r, s2_r, dpo_r = build_records_for_project(
            sample,
            max_components_per_project=args.max_components_per_project,
            repair_component_count=args.repair_component_count,
        )
        full_records.extend(full_r)
        stage1_records.extend(s1_r)
        stage2_records.extend(s2_r)
        dpo_seed_records.extend(dpo_r)

    full_train, full_val = split_by_project(full_records, args.val_ratio, args.seed)
    s1_train, s1_val = split_by_project(stage1_records, args.val_ratio, args.seed)
    s2_train, s2_val = split_by_project(stage2_records, args.val_ratio, args.seed)

    combined_train = full_train + s1_train + s2_train
    combined_val = full_val + s1_val + s2_val

    # raw outputs
    write_jsonl(out_dir / f"{STAGE_FULL}.jsonl", full_records)
    write_jsonl(out_dir / f"{STAGE_1}.jsonl", stage1_records)
    write_jsonl(out_dir / f"{STAGE_2}.jsonl", stage2_records)
    write_jsonl(out_dir / f"{STAGE_EVAL}.jsonl", eval_records)
    write_jsonl(out_dir / "dpo_seed_filewise_pairs.jsonl", dpo_seed_records)

    write_jsonl(out_dir / f"{STAGE_FULL}_train.jsonl", full_train)
    write_jsonl(out_dir / f"{STAGE_FULL}_val.jsonl", full_val)
    write_jsonl(out_dir / f"{STAGE_1}_train.jsonl", s1_train)
    write_jsonl(out_dir / f"{STAGE_1}_val.jsonl", s1_val)
    write_jsonl(out_dir / f"{STAGE_2}_train.jsonl", s2_train)
    write_jsonl(out_dir / f"{STAGE_2}_val.jsonl", s2_val)

    write_jsonl(out_dir / "sft_multistage_train.jsonl", combined_train)
    write_jsonl(out_dir / "sft_multistage_val.jsonl", combined_val)

    # OpenAI-format outputs
    write_jsonl(out_dir / "openai_sft_full_train.jsonl", to_openai_records(full_train))
    write_jsonl(out_dir / "openai_sft_full_val.jsonl", to_openai_records(full_val))
    write_jsonl(out_dir / "openai_sft_stage1_train.jsonl", to_openai_records(s1_train))
    write_jsonl(out_dir / "openai_sft_stage1_val.jsonl", to_openai_records(s1_val))
    write_jsonl(out_dir / "openai_sft_stage2_train.jsonl", to_openai_records(s2_train))
    write_jsonl(out_dir / "openai_sft_stage2_val.jsonl", to_openai_records(s2_val))
    write_jsonl(out_dir / "openai_sft_multistage_train.jsonl", to_openai_records(combined_train))
    write_jsonl(out_dir / "openai_sft_multistage_val.jsonl", to_openai_records(combined_val))

    print("=== MULTISTAGE DATASET SUMMARY ===")
    print(f"templates_root: {templates_root}")
    print(f"out_dir:        {out_dir}")
    print(f"projects_total: {len(projects)}")
    print(f"holdout_count:  {len(holdout_projects)}")
    print(f"holdout_names:  {sorted(holdout_projects)}")
    print(f"full_rows:      {len(full_records)}")
    print(f"stage1_rows:    {len(stage1_records)}")
    print(f"stage2_rows:    {len(stage2_records)}")
    print(f"dpo_seed_rows:  {len(dpo_seed_records)}")
    print(f"eval_rows:      {len(eval_records)}")
    print(f"combined_train: {len(combined_train)}")
    print(f"combined_val:   {len(combined_val)}")


if __name__ == "__main__":
    main()
