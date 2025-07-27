import requests
from AI_optimiser.config import HUGGINGFACE_TOKEN, HUGGINGFACE_MODEL_URL
from fastapi import HTTPException

def get_model(prompt: str) -> str:
    """prompt the model with the given prompt and return the response"""
    headers = {
        "Authorisation": f"Bearer {HUGGINGFACE_TOKEN}"
    }
    response = requests.post(HUGGINGFACE_MODEL_URL, headers=headers, json={"prompt": prompt})
    if response.status_code == 200:
        return response.json()["text"]
    elif response.status_code == 403:
        raise HTTPException(status_code=403, detail="Hugging Face API key is invalid")
    else:
        result = response.json()
    
    try:
        generated = result[0]["generated_text"]
        return generated.strip("### Optimized Code:\n")[-1].strip()
    except (KeyError, IndexError):
        raise HTTPException(status_code=500, detail="Failed to get response from Hugging Face model")
    
