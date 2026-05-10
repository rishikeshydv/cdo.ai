import argparse
import os
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict

import torch

if not torch.cuda.is_available():
    raise RuntimeError(
        "Qwen2.5-14B Unsloth SFT requires a CUDA-capable GPU host. "
        "Run this script on an NVIDIA/AMD/Intel GPU machine."
    )

try:
    from unsloth import FastLanguageModel
except ImportError as exc:
    raise RuntimeError(
        "Unsloth is required for this runner. Install it first, e.g. `pip install unsloth`."
    ) from exc
from datasets import load_dataset
from transformers import TrainingArguments, Trainer

# Ensure local training package is importable when running as a script
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from training.src.prompts import build_training_text, OUTPUT_MARKER, OUTPUT_END
from training.src.collators import SFTDataCollator


@dataclass
class CFG:
    model_name: str
    train_jsonl: str
    val_jsonl: str
    out_dir: str
    max_seq_len: int
    lr: float
    epochs: float
    seed: int
    per_device_train_batch_size: int
    per_device_eval_batch_size: int
    gradient_accumulation_steps: int
    warmup_ratio: float
    logging_steps: int
    eval_steps: int
    save_steps: int
    save_total_limit: int
    lora_r: int
    lora_alpha: int
    lora_dropout: float
    load_in_4bit: bool
    bf16: bool
    fp16: bool
    dataloader_num_workers: int


def load_jsonl_dataset(path: str):
    return load_dataset("json", data_files=path, split="train")


def map_to_text(example: Dict[str, Any]) -> Dict[str, Any]:
    return {"text": build_training_text(example["input"], example["output"])}


def prepare_dataset(path: str):
    ds = load_jsonl_dataset(path)
    return ds.map(map_to_text, remove_columns=ds.column_names)


def ensure_marker_tokens(model, tokenizer) -> None:
    # Keep marker strings stable so the collator can reliably locate them.
    marker_tokens = []
    vocab = tokenizer.get_vocab()
    for marker in (OUTPUT_MARKER, OUTPUT_END):
        if marker not in vocab:
            marker_tokens.append(marker)

    if marker_tokens:
        tokenizer.add_special_tokens({"additional_special_tokens": marker_tokens})
        model.resize_token_embeddings(len(tokenizer))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--config",
        default=str(SCRIPT_DIR / "configs" / "sft_qwen25_14b_unsloth.yaml"),
    )
    args = ap.parse_args()

    import yaml

    with open(args.config, "r", encoding="utf-8") as f:
        y = yaml.safe_load(f)

    cfg = CFG(**y)

    os.makedirs(cfg.out_dir, exist_ok=True)

    model, tokenizer = FastLanguageModel.from_pretrained(
        model_name=cfg.model_name,
        max_seq_length=cfg.max_seq_len,
        load_in_4bit=cfg.load_in_4bit,
        dtype=None,
    )

    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
    tokenizer.padding_side = "right"

    ensure_marker_tokens(model, tokenizer)

    model = FastLanguageModel.get_peft_model(
        model,
        r=cfg.lora_r,
        lora_alpha=cfg.lora_alpha,
        lora_dropout=cfg.lora_dropout,
        bias="none",
        target_modules=[
            "q_proj",
            "k_proj",
            "v_proj",
            "o_proj",
            "gate_proj",
            "up_proj",
            "down_proj",
        ],
        use_gradient_checkpointing="unsloth",
        random_state=cfg.seed,
        use_rslora=False,
        loftq_config=None,
    )

    train_ds = prepare_dataset(cfg.train_jsonl)
    val_ds = prepare_dataset(cfg.val_jsonl)
    collator = SFTDataCollator(tokenizer=tokenizer, max_length=cfg.max_seq_len)

    targs = TrainingArguments(
        output_dir=cfg.out_dir,
        num_train_epochs=cfg.epochs,
        learning_rate=cfg.lr,
        per_device_train_batch_size=cfg.per_device_train_batch_size,
        per_device_eval_batch_size=cfg.per_device_eval_batch_size,
        gradient_accumulation_steps=cfg.gradient_accumulation_steps,
        warmup_ratio=cfg.warmup_ratio,
        lr_scheduler_type="cosine",
        logging_steps=cfg.logging_steps,
        evaluation_strategy="steps",
        eval_steps=cfg.eval_steps,
        save_strategy="steps",
        save_steps=cfg.save_steps,
        save_total_limit=cfg.save_total_limit,
        bf16=cfg.bf16,
        fp16=cfg.fp16,
        gradient_checkpointing=True,
        optim="paged_adamw_8bit",
        remove_unused_columns=False,
        report_to="none",
        seed=cfg.seed,
        dataloader_num_workers=cfg.dataloader_num_workers,
    )

    trainer = Trainer(
        model=model,
        args=targs,
        train_dataset=train_ds,
        eval_dataset=val_ds,
        data_collator=collator,
        tokenizer=tokenizer,
    )

    trainer.train()
    trainer.save_model(cfg.out_dir)
    tokenizer.save_pretrained(cfg.out_dir)

    print(f"Saved Qwen SFT adapter to: {cfg.out_dir}")


if __name__ == "__main__":
    main()
