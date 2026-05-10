import json
import time
import argparse
from pathlib import Path
from typing import Optional
from openai import AzureOpenAI

class OpenAIFineTuner:
    def __init__(
        self,
        train_dataset_path: Path,
        val_dataset_path: Path,
        base_model: str = "gpt-4.1-2025-04-14",  # 👈 recommended
        epochs: int = 2,
        batch_size: int = 2,
        lr_mult: float = 0.08,
        poll_seconds: int = 30,
        deployment_name: str = "ai-cdo-executor",
        client: Optional[AzureOpenAI] = None,
        max_example_bytes: int = 60000,
    ):
        self.train_dataset_path = train_dataset_path
        self.val_dataset_path = val_dataset_path
        self.base_model = base_model
        self.epochs = epochs
        self.batch_size = batch_size
        self.lr_mult = lr_mult
        self.poll_seconds = poll_seconds
        self.deployment_name = deployment_name
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

        with dataset_path.open() as f:
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

                # Azure training can reject examples exceeding model context.
                # We use a strict byte cap as a practical upper-bound proxy for token count.
                joined = "\n".join(str(m.get("content", "")) for m in msgs)
                byte_count = len(joined.encode("utf-8"))
                if byte_count > self.max_example_bytes:
                    raise ValueError(
                        f"Oversized example in {dataset_name} at line {i}: "
                        f"{byte_count} bytes > max {self.max_example_bytes}. "
                        "Use a smaller/filtered dataset."
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

    def deploy_model(self, model_id: str) -> str:
        print("Deploying fine-tuned model...")

        deployment = self.client.deployments.create(
            name=self.deployment_name,
            model=model_id,
        )

        print("✓ Deployed as:", deployment.name)
        return deployment.name


    @staticmethod
    def save_model_info(model_id: str, deployment: str, path: str = "executor_model.json") -> None:
        with open(path, "w") as f:
            json.dump(
                {
                    "model_id": model_id,
                    "deployment": deployment,
                },
                f,
                indent=2,
            )
        print("✓ Model info saved to", path)


    def run(self) -> None:
        self.ensure_model_supports_finetune()
        self.validate_dataset(self.train_dataset_path, "train")
        self.validate_dataset(self.val_dataset_path, "val")

        train_id = self.upload_file(self.train_dataset_path, "train")
        val_id = self.upload_file(self.val_dataset_path, "val")

        self.wait_for_file_ready(train_id)
        self.wait_for_file_ready(val_id)

        job_id = self.start_finetune(train_id, val_id)

        model_id = self.wait_for_completion(job_id)

        deployment = self.deploy_model(model_id)

        self.save_model_info(model_id, deployment)


def main(client: AzureOpenAI, args: argparse.Namespace):
    runner = OpenAIFineTuner(
        train_dataset_path=Path(args.train_dataset),
        val_dataset_path=Path(args.val_dataset),
        base_model=args.base_model,
        epochs=args.epochs,
        batch_size=args.batch_size,
        lr_mult=args.lr_mult,
        poll_seconds=args.poll_seconds,
        deployment_name=args.deployment_name,
        client=client,
        max_example_bytes=args.max_example_bytes,
    )
    runner.run()

if __name__ == "__main__":
    import os 
    from dotenv import load_dotenv 

    parser = argparse.ArgumentParser()
    parser.add_argument("--train-dataset", default="data/openai_train.jsonl")
    parser.add_argument("--val-dataset", default="data/openai_val.jsonl")
    parser.add_argument("--base-model", default="gpt-4.1-2025-04-14")
    parser.add_argument("--epochs", type=int, default=2)
    parser.add_argument("--batch-size", type=int, default=2)
    parser.add_argument("--lr-mult", type=float, default=0.08)
    parser.add_argument("--poll-seconds", type=int, default=30)
    parser.add_argument("--deployment-name", default="ai-cdo-executor")
    parser.add_argument("--max-example-bytes", type=int, default=60000)
    args = parser.parse_args()

    BASE_DIR = Path(__file__).resolve().parent.parent
    load_dotenv(BASE_DIR / ".env.development", override=False) 
    api_key = os.getenv("AZURE_OPENAI_API_KEY") 
    endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    api_version = os.getenv("AZURE_OPENAI_API_VERSION") or "2025-04-14"

    if not api_key or not endpoint: 
        raise RuntimeError("Missing AZURE_OPENAI_API_KEY or AZURE_OPENAI_ENDPOINT") 

    client = AzureOpenAI(api_key=api_key, azure_endpoint=endpoint, api_version=api_version)

    main(client, args)
