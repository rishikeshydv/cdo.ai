import os
import json
from typing import List, Dict
from collections import defaultdict

DATASET_CATEGORIES = ["category-a", "category-b", "category-c"]
TEMPLATES_PATH = "../../../datasets/templates"

APP_DIRS = ["src/app", "app"]
COMPONENT_DIRS = ["src/components", "components"]

CANONICAL_APP_DIR = "src/app"
CANONICAL_COMPONENT_DIR = "src/components"

REQUIRED_APP_FILES = ["page.tsx", "layout.tsx", "globals.css"]
OPTIONAL_RUNTIME_FILES = [
    "package.json",
]

SKIP_LOG = defaultdict(list)

def log_skip(project: str, reason: str):
    SKIP_LOG[reason].append(project)

def read_file(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read().rstrip()

def pick_app_dir(project_path: str) -> str:
    """
    Pick a single app root when both app/ and src/app/ exist.
    Preference order is APP_DIRS (src/app first), then highest required-file coverage.
    """
    candidates = []
    for app_dir in APP_DIRS:
        full = os.path.join(project_path, app_dir)
        if os.path.isdir(full):
            score = sum(
                1 for fname in REQUIRED_APP_FILES if os.path.isfile(os.path.join(full, fname))
            )
            candidates.append((score, app_dir))

    if not candidates:
        return ""

    candidates.sort(key=lambda x: x[0], reverse=True)
    best_score = candidates[0][0]
    best = [d for s, d in candidates if s == best_score]
    for preferred in APP_DIRS:
        if preferred in best:
            return preferred
    return best[0]

def pick_component_dir(project_path: str) -> str:
    """
    Pick a single components root when both components/ and src/components/ exist.
    Preference order is COMPONENT_DIRS (src/components first), then most top-level .tsx files.
    """
    candidates = []
    for comp_dir in COMPONENT_DIRS:
        full = os.path.join(project_path, comp_dir)
        if not os.path.isdir(full):
            continue
        tsx_count = 0
        for item in os.listdir(full):
            item_path = os.path.join(full, item)
            if os.path.isfile(item_path) and item.endswith(".tsx"):
                tsx_count += 1
        candidates.append((tsx_count, comp_dir))

    if not candidates:
        return ""

    candidates.sort(key=lambda x: x[0], reverse=True)
    best_count = candidates[0][0]
    best = [d for c, d in candidates if c == best_count]
    for preferred in COMPONENT_DIRS:
        if preferred in best:
            return preferred
    return best[0]

def collect_files(project_path: str) -> List[Dict[str, str]]:
    files = []

    # runtime root files
    for fname in OPTIONAL_RUNTIME_FILES:
        fpath = os.path.join(project_path, fname)
        if os.path.isfile(fpath):
            files.append({
                "path": fname,
                "content": read_file(fpath)
            })

    app_dir = pick_app_dir(project_path)
    if not app_dir:
        return []

    app_path = os.path.join(project_path, app_dir)
    page_found = False

    for fname in REQUIRED_APP_FILES:
        fpath = os.path.join(app_path, fname)
        if os.path.isfile(fpath):
            if fname == "page.tsx":
                page_found = True

            files.append({
                "path": f"{CANONICAL_APP_DIR}/{fname}",
                "content": read_file(fpath)
            })

    if not page_found:
        return []

    comp_dir = pick_component_dir(project_path)
    if not comp_dir:
        return files

    comp_path = os.path.join(project_path, comp_dir)
    for item in sorted(os.listdir(comp_path)):
        item_path = os.path.join(comp_path, item)
        if os.path.isfile(item_path) and item.endswith(".tsx"):
            files.append({
                "path": f"{CANONICAL_COMPONENT_DIR}/{item}",
                "content": read_file(item_path)
            })

    return files

def training_dataset_creator() -> List[Dict[str, str]]:
    records: List[Dict[str, str]] = []

    for category in DATASET_CATEGORIES:
        category_path = os.path.join(TEMPLATES_PATH, category)
        if not os.path.isdir(category_path):
            print(f"[ERROR] Category path missing: {category_path}")
            continue

        for project in sorted(os.listdir(category_path)):
            project_path = os.path.join(category_path, project)
            if not os.path.isdir(project_path):
                log_skip(project, "not a directory")
                continue

            ai_cdo_path = os.path.join(project_path, "ai-cdo.txt")
            if not os.path.isfile(ai_cdo_path):
                log_skip(project, "missing ai-cdo.txt")
                continue

            with open(ai_cdo_path, "r", encoding="utf-8") as f:
                input_prompt = f.read().strip()

            if not input_prompt:
                log_skip(project, "empty ai-cdo.txt")
                continue

            files = collect_files(project_path)
            if not files:
                log_skip(project, "missing app router files")
                continue

            manifest = {
                "files": files,
                "instructions": "npm install && npm run dev"
            }

            records.append({
                "id": f"{category}-{project}",
                "project": project,
                "bucket": category[-1].upper(),
                "input": input_prompt,
                "output": json.dumps(manifest, ensure_ascii=False)
            })

    return records

if __name__ == "__main__":
    dataset = training_dataset_creator()

    output_file = "../data/sft_data.jsonl"
    with open(output_file, "w", encoding="utf-8") as f:
        for record in dataset:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")

    print("\n=== DATASET BUILD SUMMARY ===")
    print(f"Total records generated: {len(dataset)}")

    print("\n=== SKIP REASONS ===")
    for reason, projects in SKIP_LOG.items():
        print(f"\n[{reason}] ({len(projects)})")
        for p in projects[:10]:
            print(f"  - {p}")
        if len(projects) > 10:
            print(f"  ... +{len(projects) - 10} more")

    print("\n=== END OF SUMMARY ===")
