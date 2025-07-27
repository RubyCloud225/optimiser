from fastapi import FastAPI
from pydantic import BaseModel
from optimise import get_model

app = FastAPI()

class CodeRequest(BaseModel):
    code: str
    language: str = "python"

@app.post("/optimize_code")
def optimize_code(input: CodeRequest):
    optimized_code = get_model(input.code, input.language)
    return {"optimized_code": optimized_code}
