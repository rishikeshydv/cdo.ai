import os
import sys
from pathlib import Path
import argparse
from dataclasses import dataclass
from typing import Dict, Any

import torch
from datasets import load_dataset
from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    TrainingArguments,
    Trainer,
    BitsAndBytesConfig,
)
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training

# Ensure local training package is importable when running as a script
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from training.src.prompts import build_training_text
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
    gradient_accumulation_steps: int
    warmup_ratio: float
    logging_steps: int
    eval_steps: int
    save_steps: int


def load_jsonl_dataset(path: str):
    return load_dataset("json", data_files=path, split="train")

def map_to_text(example: Dict[str, Any]) -> Dict[str, Any]:
    return {"text": build_training_text(example["input"], example["output"])}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default="trainer/configs/sft.yaml")
    args = ap.parse_args()

    # simple yaml reader without extra deps
    import yaml
    with open(args.config, "r", encoding="utf-8") as f:
        y = yaml.safe_load(f)

    cfg = CFG(**y)

    os.makedirs(cfg.out_dir, exist_ok=True)

    tokenizer = AutoTokenizer.from_pretrained(cfg.model_name, use_fast=True)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    bnb_cfg = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_use_double_quant=True,
        bnb_4bit_compute_dtype=torch.bfloat16,
    )

    model = AutoModelForCausalLM.from_pretrained(
        cfg.model_name,
        quantization_config=bnb_cfg,
        torch_dtype=torch.bfloat16,
        device_map="auto",
    )

    model = prepare_model_for_kbit_training(model)

    lora = LoraConfig(
        r=32,
        lora_alpha=64,
        lora_dropout=0.05,
        bias="none",
        task_type="CAUSAL_LM",
        target_modules=["q_proj", "k_proj", "v_proj", "o_proj"],
    )
    model = get_peft_model(model, lora)

    train_ds = load_jsonl_dataset(cfg.train_jsonl).map(map_to_text, remove_columns=None)
    val_ds = load_jsonl_dataset(cfg.val_jsonl).map(map_to_text, remove_columns=None)

    collator = SFTDataCollator(tokenizer=tokenizer, max_length=cfg.max_seq_len)

    targs = TrainingArguments(
        output_dir=cfg.out_dir,
        num_train_epochs=cfg.epochs,
        learning_rate=cfg.lr,
        per_device_train_batch_size=cfg.per_device_train_batch_size,
        per_device_eval_batch_size=1,
        gradient_accumulation_steps=cfg.gradient_accumulation_steps,
        warmup_ratio=cfg.warmup_ratio,
        lr_scheduler_type="cosine",
        logging_steps=cfg.logging_steps,
        evaluation_strategy="steps",
        eval_steps=cfg.eval_steps,
        save_strategy="steps",
        save_steps=cfg.save_steps,
        save_total_limit=2,
        bf16=True,
        tf32=True,
        gradient_checkpointing=True,
        optim="paged_adamw_32bit",
        report_to="none",
        seed=cfg.seed,
        dataloader_num_workers=2,
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

    print(f"Saved SFT adapter to: {cfg.out_dir}")

if __name__ == "__main__":
    main()


#python run_sft.py --config configs/sft.yaml
