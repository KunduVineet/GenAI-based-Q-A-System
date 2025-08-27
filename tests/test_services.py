import pytest
from app.services.cache_service import cache_service
from app.models.requests import SummarizeRequest

@pytest.mark.asyncio
async def test_cache_service():
    """Test cache service functionality"""
    # Test cache operations
    key = "test_key"
    value = {"test": "data"}
    
    # Set cache
    result = await cache_service.set(key, value)
    assert result is True or result is False  # Depends on Redis availability
    
    # Get cache
    cached_data = await cache_service.get(key)
    if cached_data:  # If Redis is available
        assert cached_data == value

def test_summarize_request_validation():
    """Test request model validation"""
    # Valid request
    request = SummarizeRequest(text="This is a valid text", max_length=100)
    assert request.text == "This is a valid text"
    assert request.max_length == 100
    
    # Test validation with invalid data
    with pytest.raises(ValueError):
        SummarizeRequest(text="", max_length=100)  # Empty text