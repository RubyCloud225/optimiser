from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel
import requests
from optimise import get_model
from config import HUGGINGFACE_TOKEN, HUGGINGFACE_MODEL_URL, API_KEY

app = FastAPI()

class CodeRequest(BaseModel):
    code: str
    language: str = "python"

@app.post("/optimize_code")
def optimize_code(input: CodeRequest, x_api_key: str = Header(...)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")
    prompt = get_model(input.code)
    response = requests.post(
        HUGGINGFACE_MODEL_URL,
        headers={"Authorization": f"Bearer {HUGGINGFACE_TOKEN}"},
        json={"inputs": prompt}
    )
    if response.status_code == 200:
        optimized_code = response.json().get("generated_text", "")
        return {"optimized_code": optimized_code}
    elif response.status_code == 403:
        raise HTTPException(status_code=403, detail="Forbidden: Invalid Hugging Face token")
    
    result = response.json()
    try:
        generated = result[0]["generated_text"]
        optimize_code = generated.strip("### Optimized Code:\n")[-1].strip()
    except (KeyError, IndexError):
        raise HTTPException(status_code=500, detail="Internal Server Error: Failed to retrieve optimized code")
    
    return {
        "optimized_code": optimize_code
    }
