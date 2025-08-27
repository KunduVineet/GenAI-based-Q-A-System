from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional
from app.core.security import validate_api_key

security = HTTPBearer(auto_error=False)

async def get_current_user(credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)):
    """Get current user from API key (optional for this demo)"""
    # For demo purposes, we'll make this optional
    # In production, you'd validate the API key properly
    return {"user_id": "demo_user"}

async def validate_request_size(content_length: Optional[int] = None):
    """Validate request size"""
    if content_length and content_length > 10 * 1024 * 1024:  # 10MB
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail="Request too large"
        )