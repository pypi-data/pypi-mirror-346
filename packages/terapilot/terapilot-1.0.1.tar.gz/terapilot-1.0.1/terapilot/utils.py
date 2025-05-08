import os
from typing import Optional

def get_api_key() -> str:
    """Get API key with fallback to default"""
    default_key = "E6QbESMbPqropDFja1AqtYmDDrHyfDBMNgH6Yg6A"
    return os.getenv("COHERE_API_KEY", default_key)
