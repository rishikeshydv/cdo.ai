import importlib.util
import os
from typing import Dict, List

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig

MODEL_NAME = "meta-llama/Meta-Llama-3.1-70B-Instruct"

# ---------------- hardware + quantization -----------------------------------
_bnb_available = importlib.util.find_spec("bitsandbytes") is not None
_use_cuda = torch.cuda.is_available()
_try_quant = os.getenv("USE_QUANT", "0") == "1"
_use_quant = _bnb_available and _use_cuda and _try_quant

quant_config = (
    BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_compute_dtype=torch.bfloat16,
    )
    if _use_quant
    else None
)

device_map = "auto" if _use_cuda else {"": "cpu"}
torch_dtype = torch.bfloat16 if _use_cuda else torch.float32

# ---------------- model + tokenizer -----------------------------------------
tokenizer = AutoTokenizer.from_pretrained(
    MODEL_NAME,
    use_fast=True,
    trust_remote_code=True,
)
model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    token="HF_TOKEN",
    quantization_config=quant_config,
    device_map=device_map,
    torch_dtype=torch_dtype,
    trust_remote_code=True,
)
# Ensure pad token is set for generation
if model.generation_config.pad_token_id is None:
    model.generation_config.pad_token_id = tokenizer.eos_token_id

# ---------------- prompts ----------------------------------------------------
SYSTEM_PROMPT = (
    "You are a senior frontend engineer. Produce a JSON manifest only. "
    "No markdown, no code fences, no explanations."
)

USER_PROMPT = """
Emit a JSON manifest that describes a minimal, runnable Next.js App Router project (TypeScript + Tailwind) that satisfies the UI Intent.

MANIFEST FORMAT (required):
{
  "files": [
    {"path": "package.json", "content": "<file content>"},
    {"path": "tsconfig.json", "content": "<file content>"},
    ...
  ],
  "instructions": "npm install && npm run dev"
}

REQUIRED FILES (keep concise):
- package.json (pin Next/Tailwind/TS deps; scripts: dev, build, lint; DO NOT set "type": "module")
- next.config.js (CJS, module.exports)
- tsconfig.json (minimal, valid; jsx "preserve" or "automatic"; allowImportingTsExtensions = false)
- postcss.config.cjs (CJS)
- tailwind.config.js (CJS; include any custom colors/fonts/tokens used)
- src/app/layout.tsx
- src/app/page.tsx (single-page landing)
- src/app/globals.css (@tailwind base; components; utilities)
- src/app/favicon.ico (use https://github.com/grommet/nextjs-boilerplate/blob/master/public/favicon.ico)
- src/components/* (only if needed; keep small)

CONTENT RULES:
- App Router, TypeScript, Tailwind utilities.
- One-page, compact.
- Remote assets or inline SVG only.
- Honor any provided creative/motion/cta/proof/content_density/language_style/interaction_restraint context.
- If CTAs are delayed, keep them below the hero.
- Tone concise; no fluff; motion matches policy; conservative proof by default.

OUTPUT RULES:
- Return VALID JSON only.
- No markdown, no fences, no prose.

UI Intent: Create me a landing page for my law firm.
"""

# ---------------- generation helper -----------------------------------------
def generate_manifest(
    system_prompt: str = SYSTEM_PROMPT,
    user_prompt: str = USER_PROMPT,
    max_new_tokens: int = 1600,
) -> str:
    # messages: List[Dict[str, str]] = [
    #     {"role": "system", "content": system_prompt},
    #     {"role": "user", "content": user_prompt},
    # ]
    messages: List[Dict[str, str]] = [
        {"role": "system", "content": "You are an AI Assistant"},
        {"role": "user", "content": "Who are you?"},
    ]
    model_inputs = tokenizer.apply_chat_template(
        messages,
        add_generation_prompt=True,
        tokenize=True,
        return_dict=True,
        return_tensors="pt",
    )

    # Ensure mapping and move to device
    if isinstance(model_inputs, torch.Tensor):
        model_inputs = {"input_ids": model_inputs}
    model_inputs = {k: v.to(model.device) for k, v in model_inputs.items()}

    outputs = model.generate(
        **model_inputs,
        max_new_tokens=max_new_tokens,
        temperature=0.1,
        do_sample=False,
        eos_token_id=tokenizer.eos_token_id,
    )
    decoded = tokenizer.decode(
        outputs[0][model_inputs["input_ids"].shape[-1] :],
        skip_special_tokens=True,
    )
    return decoded.strip().strip("`")

if __name__ == "__main__":
    manifest = generate_manifest()
    print(manifest)
