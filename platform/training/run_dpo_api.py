import argparse
import json
import time
from pathlib import Path
from typing import Any, Dict, Optional

from openai import AzureOpenAI


class OpenAIDPOFineTuner:
    def __init__(
        self,
        train_dataset_path: Path,
        val_dataset_path: Path,
        base_model: str,
        n_epochs: int = 1,
        batch_size: int = 1,
        lr_mult: float = 0.05,
        beta: float = 0.1,
        poll_seconds: int = 30,
        client: Optional[AzureOpenAI] = None,
        max_example_bytes: int = 60000,
    ):
        self.train_dataset_path = train_dataset_path
        self.val_dataset_path = val_dataset_path
        self.base_model = base_model
        self.n_epochs = n_epochs
        self.batch_size = batch_size
        self.lr_mult = lr_mult
        self.beta = beta
        self.poll_seconds = poll_seconds
        self.client = client or AzureOpenAI()
        self.max_example_bytes = max_example_bytes

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
                    obj: Dict[str, Any] = json.loads(line)
                except json.JSONDecodeError:
                    raise ValueError(f"Invalid JSON in {dataset_name} at line {i}")

                input_obj = obj.get("input")
                preferred = obj.get("preferred_output")
                non_preferred = obj.get("non_preferred_output")
                if not isinstance(input_obj, dict):
                    raise ValueError(f"Invalid input object in {dataset_name} at line {i}")
                if not isinstance(preferred, list) or not preferred:
                    raise ValueError(f"Invalid preferred_output in {dataset_name} at line {i}")
                if not isinstance(non_preferred, list) or not non_preferred:
                    raise ValueError(f"Invalid non_preferred_output in {dataset_name} at line {i}")

                messages = input_obj.get("messages")
                if not isinstance(messages, list) or not messages:
                    raise ValueError(f"Invalid input.messages in {dataset_name} at line {i}")

                blob = json.dumps(obj, ensure_ascii=False)
                byte_count = len(blob.encode("utf-8"))
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

    def start_dpo_job(self, train_id: str, val_id: str) -> str:
        print("Starting DPO fine-tune job...")
        job = self.client.fine_tuning.jobs.create(
            model=self.base_model,
            training_file=train_id,
            validation_file=val_id,
            method={
                "type": "dpo",
                "dpo": {
                    "hyperparameters": {
                        "n_epochs": self.n_epochs,
                        "batch_size": self.batch_size,
                        "learning_rate_multiplier": self.lr_mult,
                        "beta": self.beta,
                    }
                },
            },
        )
        print("✓ DPO job started:", job.id)
        return job.id

    def wait_for_completion(self, job_id: str) -> str:
        print("Waiting for DPO training to complete...")
        while True:
            job = self.client.fine_tuning.jobs.retrieve(job_id)
            print(f"[{job.status}] trained_tokens={job.trained_tokens}")

            if job.status == "succeeded":
                model_id = job.fine_tuned_model
                print("✓ DPO complete:", model_id)
                return model_id
            if job.status in ("failed", "cancelled"):
                raise RuntimeError(f"DPO training failed: {job}")

            time.sleep(self.poll_seconds)

    @staticmethod
    def save_job_info(base_model: str, model_id: str, job_id: str, path: Path) -> None:
        payload = {
            "base_model": base_model,
            "dpo_model_id": model_id,
            "job_id": job_id,
        }
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        print("✓ DPO model info saved to", path)

    def run(self, output_info_path: Path, wait_for_completion: bool = True) -> None:
        self.ensure_model_supports_finetune()
        self.validate_dataset(self.train_dataset_path, "train")
        self.validate_dataset(self.val_dataset_path, "val")

        train_id = self.upload_file(self.train_dataset_path, "train")
        val_id = self.upload_file(self.val_dataset_path, "val")

        self.wait_for_file_ready(train_id)
        self.wait_for_file_ready(val_id)

        job_id = self.start_dpo_job(train_id, val_id)
        if not wait_for_completion:
            self.save_job_info(self.base_model, "", job_id, output_info_path)
            return

        model_id = self.wait_for_completion(job_id)
        self.save_job_info(self.base_model, model_id, job_id, output_info_path)


def main() -> None:
    import os
    from dotenv import load_dotenv

    parser = argparse.ArgumentParser()
    parser.add_argument("--train-dataset", required=True)
    parser.add_argument("--val-dataset", required=True)
    parser.add_argument("--base-model", required=True)
    parser.add_argument("--api-version", default=None)
    parser.add_argument("--epochs", type=int, default=1)
    parser.add_argument("--batch-size", type=int, default=1)
    parser.add_argument("--lr-mult", type=float, default=0.05)
    parser.add_argument("--beta", type=float, default=0.1)
    parser.add_argument("--poll-seconds", type=int, default=30)
    parser.add_argument("--max-example-bytes", type=int, default=60000)
    parser.add_argument("--output-info", default="training/dpo_model_info.json")
    parser.add_argument("--no-wait", action="store_true")
    args = parser.parse_args()

    base_dir = Path(__file__).resolve().parent
    load_dotenv(base_dir.parent / ".env.development", override=False)

    api_key = os.getenv("AZURE_OPENAI_API_KEY")
    endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    api_version = args.api_version or os.getenv("AZURE_OPENAI_API_VERSION") or "2024-10-21"
    if not api_key or not endpoint:
        raise RuntimeError("Missing AZURE_OPENAI_API_KEY or AZURE_OPENAI_ENDPOINT")

    client = AzureOpenAI(api_key=api_key, azure_endpoint=endpoint, api_version=api_version)
    runner = OpenAIDPOFineTuner(
        train_dataset_path=Path(args.train_dataset).resolve(),
        val_dataset_path=Path(args.val_dataset).resolve(),
        base_model=args.base_model,
        n_epochs=args.epochs,
        batch_size=args.batch_size,
        lr_mult=args.lr_mult,
        beta=args.beta,
        poll_seconds=args.poll_seconds,
        client=client,
        max_example_bytes=args.max_example_bytes,
    )
    runner.run(
        output_info_path=Path(args.output_info).resolve(),
        wait_for_completion=not args.no_wait,
    )


if __name__ == "__main__":
    main()
