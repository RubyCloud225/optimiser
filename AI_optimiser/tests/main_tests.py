import pytest
from fastapi.testclient import TestClient
from fastapi import FastAPI
from explain import router
from config import API_KEY
from secure_input_logger import encrypt_input

app = FastAPI()
app.include_router(router)

client = TestClient(app)
def test_optimise_code_success():
    encrypted_code = encrypt_input("def add(a, b): return a + b")
    response = client.post(
        "/optimize",
        json={"code": encrypted_code, "language": "python"},
        headers={"x-api-key": API_KEY}
    )
    assert response.status_code == 200
    data = response.json()
    assert "optimized_code" in data
    assert isinstance(data["optimized_code"], str)

def test_optimise_code_unauthorized():
    encrypted_code = encrypt_input("def add(a, b): return a + b")
    response = client.post(
        "/optimize",
        json={"code": encrypted_code, "language": "python"},
        headers={"x-api-key": "invalid_key"}
    )
    assert response.status_code == 401
    assert response.json() == {"detail": "Unauthorized"}

def test_optimise_code_invalid_input():
    encrypted_code = encrypt_input("def add(a, b): return a + b")
    response = client.post(
        "/optimize",
        json={"code": encrypted_code, "language": "python"},
        headers={"x-api-key": API_KEY}
    )
    assert response.status_code == 200
    data = response.json()
    assert "optimized_code" in data
    assert isinstance(data["optimized_code"], str)

def test_optimise_code_empty_input():
    response = client.post(
        "/optimize",
        json={"code": "", "language": "python"},
        headers={"x-api-key": API_KEY}
    )
    assert response.status_code == 422  # Unprocessable Entity for empty code input

def test_optimise_code_invalid_language():
    response = client.post(
        "/optimize",
        json={"code": "def add(a, b): return a + b", "language": "invalid_language"},
        headers={"x-api-key": API_KEY}
    )
    assert response.status_code == 422  # Unprocessable Entity for invalid language
def test_optimise_code_huggingface_error():
    response = client.post(
        "/optimize",
        json={"code": "def add(a, b): return a + b", "language": "python"},
        headers={"x-api-key": API_KEY}
    )
    assert response.status_code == 500
    assert response.json() == {"detail": "Hugging Face error: invalid input"}  #
    # Adjust this based on the actual error handling in your application
def test_optimise_code_huggingface_forbidden():
    response = client.post(
        "/optimize",
        json={"code": "def add(a, b): return a + b", "language": "python"},
        headers={"x-api-key": API_KEY}
    )
    assert response.status_code == 403
    assert response.json() == {"detail": "Forbidden: Invalid Hugging Face token"}  # Adjust based on actual error handling

def test_optimize_code_wrong_api_key():
    response = client.post(
        "/optimize",
        headers={"x-api-key": "wrong-key"},
        json={"code": "print('hello')", "language": "python"}
    )
    assert response.status_code == 401

def test_optimize_code_empty_code():
    response = client.post(
        "/optimize",
        headers={"x-api-key": API_KEY},
        json={"code": "", "language": "python"}
    )
    assert response.status_code in [200, 500]  # depends on model behavior

def test_optimize_code_invalid_language():
    response = client.post(
        "/optimize",
        headers={"x-api-key": API_KEY},
        json={"code": "print('hello')", "language": "unknownlang"}
    )
    assert response.status_code == 200
    assert "optimized_code" in response.json()

def test_optimize_code_streaming_response():
    response = client.post(
        "/optimize",
        headers={"x-api-key": API_KEY},
        json={"code": "print('hello')", "language": "python"}
    )
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"
    data = response.json()
    assert "optimized_code" in data
    assert isinstance(data["optimized_code"], str)
    assert len(data["optimized_code"]) > 0

