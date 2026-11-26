"""Utilities module for RAG Chat App."""

import logging
import os
from datetime import datetime
from typing import Optional


# Configure logging
def setup_logging(log_file: Optional[str] = None) -> None:
    """
    Setup logging configuration for the application.
    
    Args:
        log_file: Optional path to save log file. If None, logs to console only.
    """
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    # Create logger
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(logging.Formatter(log_format))
    logger.addHandler(console_handler)
    
    # File handler (optional)
    if log_file:
        os.makedirs(os.path.dirname(log_file) or ".", exist_ok=True)
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(logging.Formatter(log_format))
        logger.addHandler(file_handler)


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance.
    
    Args:
        name: Logger name (usually __name__)
        
    Returns:
        Logger instance
    """
    return logging.getLogger(name)


class RAGException(Exception):
    """Base exception class for RAG application."""
    pass


class DocumentLoadException(RAGException):
    """Raised when document loading fails."""
    pass


class EmbeddingException(RAGException):
    """Raised when embedding creation fails."""
    pass


class QueryException(RAGException):
    """Raised when query execution fails."""
    pass


def safe_divide(numerator: float, denominator: float, default: float = 0.0) -> float:
    """
    Safely divide two numbers.
    
    Args:
        numerator: The numerator
        denominator: The denominator
        default: Default value if denominator is 0
        
    Returns:
        Result of division or default value
    """
    try:
        return numerator / denominator if denominator != 0 else default
    except (TypeError, ZeroDivisionError):
        return default


def format_file_size(size_bytes: int) -> str:
    """
    Format bytes to human-readable file size.
    
    Args:
        size_bytes: Size in bytes
        
    Returns:
        Human-readable file size string
    """
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} TB"


def get_timestamp() -> str:
    """
    Get current timestamp in ISO format.
    
    Returns:
        ISO format timestamp
    """
    return datetime.now().isoformat()


def print_section(title: str, char: str = "=") -> None:
    """
    Print a formatted section header.
    
    Args:
        title: Section title
        char: Character to use for border
    """
    border = char * (len(title) + 4)
    print(f"\n{border}")
    print(f"{char} {title} {char}")
    print(f"{border}\n")


def validate_file_type(filename: str, allowed_types: list) -> bool:
    """
    Validate that file extension is in allowed types.
    
    Args:
        filename: Name of the file
        allowed_types: List of allowed extensions (e.g., ['pdf', 'txt'])
        
    Returns:
        True if file type is allowed
    """
    file_ext = os.path.splitext(filename)[1].lstrip('.').lower()
    return file_ext in [t.lower() for t in allowed_types]


def get_available_models() -> dict:
    """
    Get dictionary of available OpenAI models.
    
    Returns:
        Dictionary with model names and descriptions
    """
    return {
        "gpt-3.5-turbo": {
            "name": "GPT-3.5 Turbo",
            "cost": "Fastest and most economical",
            "recommended": True
        },
        "gpt-4": {
            "name": "GPT-4",
            "cost": "More capable but slower and more expensive",
            "recommended": False
        },
        "gpt-4-turbo": {
            "name": "GPT-4 Turbo",
            "cost": "Better performance than GPT-4 at lower cost",
            "recommended": False
        }
    }


def chunk_size_recommendation(document_count: int) -> int:
    """
    Get recommended chunk size based on document count.
    
    Args:
        document_count: Number of documents
        
    Returns:
        Recommended chunk size
    """
    if document_count <= 5:
        return 500
    elif document_count <= 20:
        return 1000
    else:
        return 1500


# Setup logging when module is imported
setup_logging()
