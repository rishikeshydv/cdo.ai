import os
from typing import List, Dict
from collections import defaultdict

DATASET_CATEGORIES = ["category-a","category-b","category-c"]
TEMPLATES_PATH = "../../../datasets/templates"

APP_DIRS = ["app", "src/app"]
COMPONENT_DIRS = ["components", "src/components"]

REQUIRED_APP_FILES = ["page.tsx", "layout.tsx", "globals.css"]

SKIP_LOG = defaultdict(list)

def log_skip(project: str, reason: str):
    SKIP_LOG[reason].append(project)

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

            # ---- ai-cdo.txt ----
            ai_cdo_path = os.path.join(project_path, "ai-cdo.txt")
            if not os.path.isfile(ai_cdo_path):
                log_skip(project, "missing ai-cdo.txt")
                continue

            with open(ai_cdo_path, "r", encoding="utf-8") as f:
                input_prompt = f.read().strip()

            if not input_prompt:
                log_skip(project, "empty ai-cdo.txt")
                continue

            output_chunks: List[str] = []

            # ---- app router ----
            app_found = False
            page_found = False

            for app_dir in APP_DIRS:
                app_path = os.path.join(project_path, app_dir)
                if not os.path.isdir(app_path):
                    continue

                app_found = True

                for fname in REQUIRED_APP_FILES:
                    fpath = os.path.join(app_path, fname)
                    if not os.path.isfile(fpath):
                        continue

                    if fname == "page.tsx":
                        page_found = True

                    with open(fpath, "r", encoding="utf-8") as f:
                        rel = os.path.relpath(fpath, project_path)
                        output_chunks.append(
                            f"FILE: {rel}\n"
                            "--------------------\n"
                            f"{f.read().rstrip()}\n"
                        )

            if not app_found:
                log_skip(project, "no app/ or src/app/")
                continue

            if not page_found:
                log_skip(project, "missing page.tsx")
                continue

            # ---- components (root only) ----
            for comp_dir in COMPONENT_DIRS:
                comp_path = os.path.join(project_path, comp_dir)
                if not os.path.isdir(comp_path):
                    continue

                for item in sorted(os.listdir(comp_path)):
                    item_path = os.path.join(comp_path, item)

                    if os.path.isfile(item_path) and item.endswith(".tsx"):
                        with open(item_path, "r", encoding="utf-8") as f:
                            rel = os.path.relpath(item_path, project_path)
                            output_chunks.append(
                                f"FILE: {rel}\n"
                                "--------------------\n"
                                f"{f.read().rstrip()}\n"
                            )

            if not output_chunks:
                log_skip(project, "no output files collected")
                continue

            records.append(
                {
                    "id": f"{category}-{project}",
                    "project": project,
                    "bucket": category[-1].upper(),
                    "input": input_prompt,
                    "output": "\n".join(output_chunks).strip(),
                }
            )

    return records

if __name__ == "__main__":
    dataset = training_dataset_creator()
        #create sft_data_jsonl file at ../data
    output_file = "../data/sft_data.jsonl"
    with open(output_file, "w", encoding="utf-8") as f:
        for record in dataset:
            f.write(f"{record}\n")

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