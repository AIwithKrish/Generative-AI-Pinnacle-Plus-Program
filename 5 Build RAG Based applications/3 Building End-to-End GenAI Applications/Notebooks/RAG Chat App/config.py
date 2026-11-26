"""Configuration and utility functions for the RAG Chat App."""

import os
from typing import Optional
from dotenv import load_dotenv


# Load environment variables
load_dotenv()


# API Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
OPENAI_TEMPERATURE = float(os.getenv("OPENAI_TEMPERATURE", "0.7"))

# Document Processing Configuration
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "1000"))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "200"))

# Vector Store Configuration
VECTOR_STORE_PATH = os.getenv("VECTOR_STORE_PATH", "./vector_store")
RETRIEVAL_K = int(os.getenv("RETRIEVAL_K", "3"))

# File Upload Configuration
ALLOWED_FILE_TYPES = ["pdf", "txt"]
MAX_UPLOAD_SIZE_MB = int(os.getenv("MAX_UPLOAD_SIZE_MB", "50"))

# Application Settings
APP_TITLE = "RAG Chat Application"
APP_ICON = ""


def validate_api_key(api_key: Optional[str] = None) -> bool:
    """
    Validate that an OpenAI API key is provided.
    
    Args:
        api_key: Optional API key to validate. If None, checks environment.
        
    Returns:
        True if API key is valid, False otherwise
    """
    key = api_key or OPENAI_API_KEY
    return key is not None and isinstance(key, str) and len(key.strip()) > 0


def get_data_directory() -> str:
    """
    Get the path to the data directory.
    
    Returns:
        Path to the data directory
    """
    data_dir = os.path.join(os.path.dirname(__file__), "data")
    os.makedirs(data_dir, exist_ok=True)
    return data_dir


def get_sample_documents() -> list:
    """
    Get list of sample documents in the data directory.
    
    Returns:
        List of sample document paths
    """
    data_dir = get_data_directory()
    documents = []
    
    for file in os.listdir(data_dir):
        if file.endswith(('.pdf', '.txt')):
            documents.append(os.path.join(data_dir, file))
    
    return documents
