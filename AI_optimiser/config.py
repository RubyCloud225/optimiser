import os
from dotenv import load_dotenv

load_dotenv()

#hugging face 
HUGGINGFACE_TOKEN = os.getenv("HUGGINGFACE_TOKEN")
HUGGINGFACE_MODEL_URL = os.getenv("HUGGINGFACE_MODEL_URL")
# API key for VS Code extension access
API_KEY = os.getenv("API_KEY")