from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
import importlib.util
import torch

MODEL_NAME = "Qwen/Qwen2.5-Coder-7B-Instruct"

_bnb_available = importlib.util.find_spec("bitsandbytes") is not None
_use_cuda = torch.cuda.is_available()
_use_quant = _bnb_available and _use_cuda

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
dtype = torch.float16 if _use_cuda else torch.float32

tokenizer = AutoTokenizer.from_pretrained(
    MODEL_NAME,
    trust_remote_code=True,
    use_fast=True
)

model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    quantization_config=quant_config,
    device_map=device_map,
    dtype=dtype,
    trust_remote_code=True,
)

# Ensure a valid pad token for generation.
model.generation_config.pad_token_id = tokenizer.eos_token_id

messages = [
    {"role": "user", "content": "Who are you?"},
]
inputs = tokenizer.apply_chat_template(
	messages,
	add_generation_prompt=True,
	tokenize=True,
	return_dict=True,
	return_tensors="pt",
).to(model.device)

outputs = model.generate(**inputs, max_new_tokens=40)
print(tokenizer.decode(outputs[0][inputs["input_ids"].shape[-1]:]))
