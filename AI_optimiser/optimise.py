import requests
from fastapi import HTTPException
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

generator = None
tokenizer = None

def load_local_model():
    global generator, tokenizer
    if generator is None or tokenizer is None:
        tokenizer = AutoTokenizer.from_pretrained("gpt2")
        generator = AutoModelForCausalLM.from_pretrained("gpt2")

# Cache on startup
load_local_model()

def get_model(prompt: str) -> str:
    """prompt the model with the given prompt and return the response"""
    try:
        input_ids = tokenizer(prompt, return_tensors="pt").input_ids
        outputs = generator.generate(input_ids, max_new_tokens=100)
        return tokenizer.decode(outputs[0], skip_special_tokens=True)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Local model failed: {str(e)}")
