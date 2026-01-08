from dataclasses import dataclass
from typing import List, Dict, Any, Optional

import torch
from transformers import PreTrainedTokenizerBase

from .prompts import OUTPUT_MARKER

@dataclass
class SFTDataCollator:
    tokenizer: PreTrainedTokenizerBase
    max_length: int

    def __call__(self, features: List[Dict[str, Any]]) -> Dict[str, torch.Tensor]:
        """
        Each feature must have 'text' which is:
          input + "\n\n<OUTPUT>\n" + output + "\n</OUTPUT>\n"

        We mask loss on everything before the <OUTPUT> marker.
        """
        texts = [f["text"] for f in features]

        batch = self.tokenizer(
            texts,
            padding=True,
            truncation=True,
            max_length=self.max_length,
            return_tensors="pt",
        )

        input_ids = batch["input_ids"]
        attention_mask = batch["attention_mask"]

        labels = input_ids.clone()

        # Tokenize marker once
        marker_ids = self.tokenizer(OUTPUT_MARKER, add_special_tokens=False)["input_ids"]
        if not marker_ids:
            raise ValueError("OUTPUT_MARKER tokenization produced empty ids")

        # For each row, find marker start index and mask before it
        for i in range(input_ids.size(0)):
            row = input_ids[i].tolist()
            start = _find_subseq(row, marker_ids)
            if start is None:
                # If marker is missing due to truncation or bad data, drop loss entirely
                labels[i, :] = -100
                continue
            # mask up to end of marker token sequence
            mask_upto = start + len(marker_ids)
            labels[i, :mask_upto] = -100

        return {
            "input_ids": input_ids,
            "attention_mask": attention_mask,
            "labels": labels,
        }

def _find_subseq(seq: List[int], sub: List[int]) -> Optional[int]:
    # naive subsequence search is fine (marker is short)
    n, m = len(seq), len(sub)
    if m == 0 or m > n:
        return None
    for i in range(n - m + 1):
        if seq[i:i+m] == sub:
            return i
    return None
