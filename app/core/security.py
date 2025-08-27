import hashlib
import hmac
from typing import Optional

def create_cache_key(prefix: str, content: str) -> str:
    """Create a consistent cache key"""
    content_hash = hashlib.md5(content.encode()).hexdigest()
    return f"{prefix}:{content_hash}"

def validate_api_key(api_key: Optional[str]) -> bool:
    """Validate API key if needed"""
    # For now, just check if it exists
    return api_key is not None