import argparse
import ast
import json
from pathlib import Path
import os
import numpy as np
from transformers import AutoTokenizer

DEFAULT_MODEL = "meta-llama/Meta-Llama-3.1-70B-Instruct"
# Fallback HF token; will be overridden by HF_TOKEN env if set.
DEFAULT_TOKEN = os.getenv("HF_TOKEN", "HF_TOKEN")


def _parse_record(line: str):
    """Parse a JSONL line; fall back to Python literal repr."""
    try:
        return json.loads(line)
    except json.JSONDecodeError:
        try:
            return ast.literal_eval(line)
        except Exception:
            return None


def _normalize_text(val: str) -> str:
    """Fix escaped newlines and '/n' artifacts in the dataset."""
    return val.replace("\\n", "\n").replace("/n", "\n")


def main():
    default_in = Path(__file__).resolve().parent.parent / "data" / "sft_raw_jsonl"

    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--in_jsonl",
        default=str(default_in),
        help="Path to JSONL (defaults to ../data/sft_raw_jsonl)",
    )
    ap.add_argument(
        "--model_name",
        default=DEFAULT_MODEL,
        help=f"Tokenizer/model name (default: {DEFAULT_MODEL})",
    )
    ap.add_argument("--max_samples", type=int, default=0, help="0 = all")
    args = ap.parse_args()

    tok = AutoTokenizer.from_pretrained(
        args.model_name,
        use_fast=True,
        token=DEFAULT_TOKEN,
    )

    lengths = []
    n = 0
    with open(args.in_jsonl, "r", encoding="utf-8") as f:
        for line in f:
            rec = _parse_record(line)
            if not rec or "input" not in rec or "output" not in rec:
                continue
            text = (
                _normalize_text(rec["input"]).rstrip()
                + "\n\n<OUTPUT>\n"
                + _normalize_text(rec["output"]).rstrip()
                + "\n</OUTPUT>\n"
            )
            ids = tok(text, add_special_tokens=True, truncation=False)["input_ids"]
            lengths.append(len(ids))
            n += 1
            if args.max_samples and n >= args.max_samples:
                break

    arr = np.array(lengths, dtype=np.int32)

    def pct(p):
        return int(np.percentile(arr, p))

    print("\n=== TOKEN LENGTH STATS ===")
    print(f"samples: {len(arr)}")
    print(f"p50: {pct(50)}")
    print(f"p75: {pct(75)}")
    print(f"p90: {pct(90)}")
    print(f"p95: {pct(95)}  <-- recommended max_seq_len")
    print(f"p99: {pct(99)}")
    print(f"max: {int(arr.max())}")

if __name__ == "__main__":
    main()


# to run in console
# export HF_TOKEN=HF_TOKEN
# python datasets/training/scripts/token_stats.py --model_name meta-llama/Meta-Llama-3.1-70B-Instruct
