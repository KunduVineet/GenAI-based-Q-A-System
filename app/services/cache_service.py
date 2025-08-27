import json
import redis
from typing import Optional, Any
from app.core.config import settings
from app.core.security import create_cache_key
from app.utils.logger import app_logger

class CacheService:
    """Redis caching service"""
    
    def __init__(self):
        try:
            self.redis_client = redis.from_url(settings.redis_url, decode_responses=True)
            self.redis_client.ping()
            app_logger.info("Connected to Redis successfully")
        except Exception as e:
            app_logger.error(f"Failed to connect to Redis: {str(e)}")
            self.redis_client = None
    
    async def get(self, key: str) -> Optional[Any]:
        """Get value from cache"""
        if not self.redis_client:
            return None
        
        try:
            cached_data = self.redis_client.get(key)
            if cached_data:
                app_logger.info(f"Cache hit for key: {key}")
                return json.loads(cached_data)
        except Exception as e:
            app_logger.error(f"Error getting cache for key {key}: {str(e)}")
        
        return None
    
    async def set(self, key: str, value: Any, ttl: int = None) -> bool:
        """Set value in cache"""
        if not self.redis_client:
            return False
        
        try:
            ttl = ttl or settings.cache_ttl
            serialized_value = json.dumps(value, default=str)
            result = self.redis_client.setex(key, ttl, serialized_value)
            app_logger.info(f"Cache set for key: {key}, TTL: {ttl}")
            return result
        except Exception as e:
            app_logger.error(f"Error setting cache for key {key}: {str(e)}")
            return False
    
    async def delete(self, key: str) -> bool:
        """Delete value from cache"""
        if not self.redis_client:
            return False
        
        try:
            result = self.redis_client.delete(key)
            app_logger.info(f"Cache deleted for key: {key}")
            return bool(result)
        except Exception as e:
            app_logger.error(f"Error deleting cache for key {key}: {str(e)}")
            return False
    
    def create_key(self, prefix: str, content: str) -> str:
        """Create cache key"""
        return create_cache_key(prefix, content)

cache_service = CacheService()