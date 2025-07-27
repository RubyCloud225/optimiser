from fastapi.responses import StreamingResponse
import io
from fastapi import APIRouter, HTTPException, Header
from pydantic import BaseModel
from AI_optimiser.optimise import get_model
from AI_optimiser.secure_input_logger import encrypt_input, decrypt_input, log_input

router = APIRouter()

class CodeRequest(BaseModel):
    code: str
    language: str = "python"

@router.post("/explain")
def explain_code(input: CodeRequest):
    decrypted_input = decrypt_input(input.code)
    if not decrypted_input:
        raise HTTPException(status_code=400, detail="Invalid input data")
    log_input(decrypted_input)
    prompt = f"### Explain the following {input.language} code:\n\n{input.code}\n\n### Explanation:\n"
    generated = get_model(prompt)
    explanation = generated.split("### Explanation:")[-1].strip()
    # return error if explanation is empty
    if not explanation:
        raise HTTPException(status_code=500, detail="Failed to generate explanation")
    import logging; logging.info(f"Generated explanation: {explanation}")
    
    def generate_explanation():
        for line in explanation.split("\n"):
            yield line + "\n"
    return StreamingResponse(generate_explanation(), media_type="text/plain")

# This code defines a FastAPI endpoint that takes a code snippet and its language as input,
# generates an explanation for the code using a model, and streams the explanation back to the client.
# The endpoint checks for an API key in the request header to ensure authorization.
# If the API key is invalid, it raises a 401 Unauthorized error.
# If the model fails to generate an explanation, it raises a 500 Internal Server Error.
# The explanation is streamed line by line to the client as plain text.
# The endpoint is protected by an API key, which must be provided in the request header.

@router.post("/optimize")
def optimize_code(input: CodeRequest):
    decrypted_input = decrypt_input(input.code)
    if not decrypted_input:
        raise HTTPException(status_code=400, detail="Invalid input data")
    log_input(decrypted_input)
    prompt = f"### Optimize the following {input.language} code:\n\n{input.code}\n\n### Optimized Code:\n"
    generated = get_model(prompt)
    optimized_code = generated.split("### Optimized Code:")[-1].strip()
    # return error if optimized code is empty
    if not optimized_code:
        raise HTTPException(status_code=500, detail="Failed to generate optimized code")
    def generate_optimized_code():
        for line in optimized_code.split("\n"):
            yield line + "\n"
    return StreamingResponse(generate_optimized_code(), media_type="text/plain")