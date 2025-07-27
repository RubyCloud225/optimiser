import pytest
from fastapi.testclient import TestClient
from fastapi import FastAPI
from explain import router
from config import API_KEY
from secure_input_logger import encrypt_input

app = FastAPI()
app.include_router(router)

client = TestClient(app)

def test_explain_code_success():
    response = client.post(
        "/explain",
        headers={"x-api-key": API_KEY},
        json={"code": encrypt_input("def add(a, b): return a + b"), "language": "python"}
    )
    assert response.status_code == 500
    assert isinstance(response.text, str)
    assert len(response.text.strip()) > 0

def test_explain_code_missing_api_key():
    response = client.post(
        "/explain",
        json={"code": encrypt_input("print('hello')"), "language": "python"}
    )
    assert response.status_code == 422  # missing header

def test_explain_code_invalid_api_key():
    response = client.post(
        "/explain",
        headers={"x-api-key": "invalid"},
        json={"code": encrypt_input("print('hello')"), "language": "python"}
    )
    assert response.status_code == 401

def test_explain_code_empty_input():
    response = client.post(
        "/explain",
        headers={"x-api-key": API_KEY},
        json={"code": encrypt_input(""), "language": "python"}
    )
    assert response.status_code == 400  # empty input should be rejected

def test_explain_code_invalid_language():
    response = client.post(
        "/explain",
        headers={"x-api-key": API_KEY},
        json={"code": encrypt_input("print('hello')"), "language": "unknown"}
    )
    assert response.status_code == 500  # unsupported language causes model error

# Simulate a VS Code extension request to the /explain endpoint.
def test_explain_code_from_vscode_request():
    vscode_simulated_code = """
def greet(name):
    print(f"Hello, {name}")
"""
    response = client.post(
        "/explain",
        headers={"x-api-key": API_KEY},
        json={"code": encrypt_input(vscode_simulated_code.strip()), "language": "python"}
    )
    assert response.status_code in [200, 500]
    assert isinstance(response.text, str)
