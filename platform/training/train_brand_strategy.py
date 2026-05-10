import argparse
import csv
import json
import os
import random
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from dotenv import load_dotenv
from openai import AzureOpenAI

BRAND_SYSTEM_PROMPT = (
    "You are a brand design inference engine that predicts brand-level traits "
    "from strategy and business context. Return JSON only with keys: "
    "tone, color_style, typography, density, motion, radius, icons."
)

PROMPT_TEMPLATES = [
    "Brand: {brand}. Return the brand traits JSON.",
    (
        "USER PROMPT:\n"
        "Design a premium product website inspired by {brand}.\n\n"
        "STEP 2 CONTEXT:\n"
        "{{\"industry\": \"saas\", \"trust_sensitivity\": \"medium\", \"risk_tolerance_bucket\": \"B\"}}\n\n"
        "SELECTED STRATEGY:\n"
        "{{\"strategy_id\": \"balanced_clarity_conversion\", \"intent\": \"convert_with_credibility\"}}\n\n"
        "Infer brand traits JSON only."
    ),
    (
        "USER PROMPT:\n"
        "Create a conservative trust-first UI direction with {brand}-like polish.\n\n"
        "STEP 2 CONTEXT:\n"
        "{{\"industry\": \"fintech\", \"trust_sensitivity\": \"high\", \"risk_tolerance_bucket\": \"A\"}}\n\n"
        "SELECTED STRATEGY:\n"
        "{{\"strategy_id\": \"proof_led_reassurance\", \"intent\": \"reduce_anxiety_then_prompt_action\"}}\n\n"
        "Return only JSON traits."
    ),
]


class OpenAIBrandFineTuner:
    def __init__(
        self,
        train_dataset_path: Path,
        val_dataset_path: Path,
        base_model: str = "gpt-4.1-2025-04-14",
        epochs: int = 2,
        batch_size: int = 2,
        lr_mult: float = 0.08,
        poll_seconds: int = 30,
        max_example_bytes: int = 30000,
        deploy_name: str = "",
        client: Optional[AzureOpenAI] = None,
    ):
        self.train_dataset_path = train_dataset_path
        self.val_dataset_path = val_dataset_path
        self.base_model = base_model
        self.epochs = epochs
        self.batch_size = batch_size
        self.lr_mult = lr_mult
        self.poll_seconds = poll_seconds
        self.max_example_bytes = max_example_bytes
        self.deploy_name = deploy_name.strip()
        self.client = client or AzureOpenAI()

    def ensure_model_supports_finetune(self) -> None:
        model = self.client.models.retrieve(self.base_model)
        capabilities = getattr(model, "capabilities", None) or {}
        supports = bool(capabilities.get("fine_tune")) if isinstance(capabilities, dict) else False
        if not supports:
            raise RuntimeError(
                f"Base model '{self.base_model}' is not fine-tunable on this Azure resource. "
                f"Model capabilities: {capabilities}"
            )

    def validate_dataset(self, dataset_path: Path, dataset_name: str) -> None:
        if not dataset_path.exists():
            raise FileNotFoundError(dataset_path)

        with dataset_path.open("r", encoding="utf-8") as f:
            for i, line in enumerate(f, 1):
                try:
                    obj = json.loads(line)
                except json.JSONDecodeError:
                    raise ValueError(f"Invalid JSON in {dataset_name} at line {i}")

                msgs = obj.get("messages")
                if not isinstance(msgs, list) or len(msgs) < 3:
                    raise ValueError(f"Invalid messages format in {dataset_name} at line {i}")

                roles = [m.get("role") for m in msgs]
                if roles[:3] != ["system", "user", "assistant"]:
                    raise ValueError(f"Unexpected roles in {dataset_name} at line {i}: {roles}")

                joined = "\n".join(str(m.get("content", "")) for m in msgs)
                byte_count = len(joined.encode("utf-8"))
                if byte_count > self.max_example_bytes:
                    raise ValueError(
                        f"Oversized example in {dataset_name} at line {i}: "
                        f"{byte_count} bytes > max {self.max_example_bytes}"
                    )

        print(f"✓ Dataset validation passed ({dataset_name})")

    def upload_file(self, dataset_path: Path, dataset_name: str) -> str:
        print(f"Uploading dataset ({dataset_name}): {dataset_path}")
        with dataset_path.open("rb") as f:
            file = self.client.files.create(file=f, purpose="fine-tune")
        print(f"✓ Uploaded ({dataset_name}): {file.id}")
        return file.id

    def wait_for_file_ready(self, file_id: str) -> None:
        print("Waiting for file processing:", file_id)
        while True:
            f = self.client.files.retrieve(file_id)
            if f.status in ("processed", "ready"):
                print("✓ File ready:", file_id)
                return
            if f.status in ("failed", "error"):
                raise RuntimeError(f"File processing failed: {f}")
            time.sleep(3)

    def start_finetune(self, train_id: str, val_id: str) -> str:
        print("Starting fine-tune job...")
        job = self.client.fine_tuning.jobs.create(
            model=self.base_model,
            training_file=train_id,
            validation_file=val_id,
            hyperparameters={
                "n_epochs": self.epochs,
                "batch_size": self.batch_size,
                "learning_rate_multiplier": self.lr_mult,
            },
        )
        print("✓ Job started:", job.id)
        return job.id

    def wait_for_completion(self, job_id: str) -> str:
        print("Waiting for training to complete...")
        while True:
            job = self.client.fine_tuning.jobs.retrieve(job_id)
            print(f"[{job.status}] trained_tokens={job.trained_tokens}")

            if job.status == "succeeded":
                model_id = job.fine_tuned_model
                print("✓ Training complete:", model_id)
                return model_id

            if job.status in ("failed", "cancelled"):
                raise RuntimeError(f"Training failed: {job}")

            time.sleep(self.poll_seconds)

    def maybe_deploy(self, model_id: str) -> str:
        if not self.deploy_name:
            return ""

        if not hasattr(self.client, "deployments"):
            print("⚠️ Skipping deployment: current SDK/client has no deployments API")
            return ""

        try:
            print("Deploying fine-tuned model...")
            deployment = self.client.deployments.create(name=self.deploy_name, model=model_id)
            print("✓ Deployed as:", deployment.name)
            return deployment.name
        except Exception as exc:
            print(f"⚠️ Deployment failed: {exc}")
            return ""

    @staticmethod
    def save_model_info(path: Path, payload: Dict[str, Any]) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        print("✓ Model info saved to", path)

    def run(self, output_info_path: Path, wait: bool = True) -> None:
        self.ensure_model_supports_finetune()
        self.validate_dataset(self.train_dataset_path, "train")
        self.validate_dataset(self.val_dataset_path, "val")

        train_id = self.upload_file(self.train_dataset_path, "train")
        val_id = self.upload_file(self.val_dataset_path, "val")

        self.wait_for_file_ready(train_id)
        self.wait_for_file_ready(val_id)

        job_id = self.start_finetune(train_id, val_id)
        if not wait:
            self.save_model_info(
                output_info_path,
                {
                    "job_id": job_id,
                    "base_model": self.base_model,
                    "train_file_id": train_id,
                    "val_file_id": val_id,
                    "fine_tuned_model": "",
                    "deployment": "",
                },
            )
            return

        model_id = self.wait_for_completion(job_id)
        deployment = self.maybe_deploy(model_id)

        self.save_model_info(
            output_info_path,
            {
                "job_id": job_id,
                "base_model": self.base_model,
                "train_file_id": train_id,
                "val_file_id": val_id,
                "fine_tuned_model": model_id,
                "deployment": deployment,
            },
        )


def normalize_traits(row: Dict[str, str]) -> Dict[str, str]:
    return {
        "tone": row["Tone"].strip(),
        "color_style": row["Color style"].strip(),
        "typography": row["Typography"].strip(),
        "density": row["Density"].strip(),
        "motion": row["Motion"].strip(),
        "radius": row["Radius"].strip(),
        "icons": row["Icons"].strip(),
    }


def build_messages(brand: str, traits: Dict[str, str], template: str) -> Dict[str, Any]:
    return {
        "messages": [
            {"role": "system", "content": BRAND_SYSTEM_PROMPT},
            {"role": "user", "content": template.format(brand=brand)},
            {"role": "assistant", "content": json.dumps(traits, ensure_ascii=False)},
        ]
    }


def load_brand_rows(csv_path: Path) -> List[Tuple[str, Dict[str, str]]]:
    rows: List[Tuple[str, Dict[str, str]]] = []
    with csv_path.open(newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        required = {"Brand", "Tone", "Color style", "Typography", "Density", "Motion", "Radius", "Icons"}
        if not required.issubset(set(reader.fieldnames or [])):
            raise ValueError(f"CSV missing required columns: {sorted(required)}")

        for row in reader:
            brand = row["Brand"].strip()
            if not brand:
                continue
            rows.append((brand, normalize_traits(row)))
    return rows


def write_jsonl(path: Path, rows: List[Dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")


def build_train_val_from_csv(
    csv_path: Path,
    train_out: Path,
    val_out: Path,
    val_ratio: float,
    seed: int,
    prompts_per_brand: int,
) -> Tuple[int, int, int]:
    base_rows = load_brand_rows(csv_path)
    if len(base_rows) < 5:
        raise ValueError("Brand CSV is too small; need at least 5 rows for train/val split")

    rng = random.Random(seed)
    rng.shuffle(base_rows)

    val_n = max(1, int(len(base_rows) * val_ratio))
    val_brands = {b for b, _ in base_rows[:val_n]}

    template_count = min(len(PROMPT_TEMPLATES), max(1, prompts_per_brand))
    templates = PROMPT_TEMPLATES[:template_count]

    train_records: List[Dict[str, Any]] = []
    val_records: List[Dict[str, Any]] = []

    for brand, traits in base_rows:
        target = val_records if brand in val_brands else train_records
        for t in templates:
            target.append(build_messages(brand, traits, t))

    write_jsonl(train_out, train_records)
    write_jsonl(val_out, val_records)
    return len(base_rows), len(train_records), len(val_records)


def main() -> None:
    parser = argparse.ArgumentParser()
    root = Path(__file__).resolve().parents[2]
    training_dir = Path(__file__).resolve().parent

    parser.add_argument("--csv-path", default=str(root / "datasets/brand_strategy_engine_data.csv"))
    parser.add_argument("--train-jsonl", default=str(training_dir / "data/brand_strategy_train.jsonl"))
    parser.add_argument("--val-jsonl", default=str(training_dir / "data/brand_strategy_val.jsonl"))
    parser.add_argument("--val-ratio", type=float, default=0.2)
    parser.add_argument("--seed", type=int, default=1337)
    parser.add_argument("--prompts-per-brand", type=int, default=3)

    parser.add_argument("--base-model", default="gpt-4.1-2025-04-14")
    parser.add_argument("--epochs", type=int, default=2)
    parser.add_argument("--batch-size", type=int, default=2)
    parser.add_argument("--lr-mult", type=float, default=0.08)
    parser.add_argument("--poll-seconds", type=int, default=30)
    parser.add_argument("--max-example-bytes", type=int, default=30000)
    parser.add_argument("--deploy-name", default="")
    parser.add_argument("--output-info", default=str(training_dir / "brand_model_info.json"))
    parser.add_argument("--no-wait", action="store_true")
    parser.add_argument("--api-version", default=None)
    parser.add_argument("--prepare-only", action="store_true")
    args = parser.parse_args()

    base_dir = Path(__file__).resolve().parent.parent
    load_dotenv(base_dir / ".env.development", override=False)

    api_key = os.getenv("AZURE_OPENAI_API_KEY")
    endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    api_version = args.api_version or os.getenv("AZURE_OPENAI_API_VERSION") or "2024-10-21"

    if not api_key or not endpoint:
        raise RuntimeError("Missing AZURE_OPENAI_API_KEY or AZURE_OPENAI_ENDPOINT")

    csv_path = Path(args.csv_path).resolve()
    train_jsonl = Path(args.train_jsonl).resolve()
    val_jsonl = Path(args.val_jsonl).resolve()

    brands, train_rows, val_rows = build_train_val_from_csv(
        csv_path=csv_path,
        train_out=train_jsonl,
        val_out=val_jsonl,
        val_ratio=args.val_ratio,
        seed=args.seed,
        prompts_per_brand=args.prompts_per_brand,
    )

    print("=== BRAND DATASET SUMMARY ===")
    print(f"csv_brands:      {brands}")
    print(f"train_rows:      {train_rows}")
    print(f"val_rows:        {val_rows}")
    print(f"train_jsonl:     {train_jsonl}")
    print(f"val_jsonl:       {val_jsonl}")

    if args.prepare_only:
        print("✓ Dataset prepared only; skipping fine-tune launch")
        return

    client = AzureOpenAI(api_key=api_key, azure_endpoint=endpoint, api_version=api_version)
    runner = OpenAIBrandFineTuner(
        train_dataset_path=train_jsonl,
        val_dataset_path=val_jsonl,
        base_model=args.base_model,
        epochs=args.epochs,
        batch_size=args.batch_size,
        lr_mult=args.lr_mult,
        poll_seconds=args.poll_seconds,
        max_example_bytes=args.max_example_bytes,
        deploy_name=args.deploy_name,
        client=client,
    )
    runner.run(output_info_path=Path(args.output_info).resolve(), wait=not args.no_wait)


if __name__ == "__main__":
    main()
