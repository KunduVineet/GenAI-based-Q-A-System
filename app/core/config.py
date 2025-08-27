import os
from typing import Optional
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """Application settings"""
    
    # App settings
    debug: bool = False
    app_name: str = "AI Backend Service"
    version: str = "1.0.0"
    
    # API settings
    api_v1_prefix: str = "/api/v1"
    max_request_size: int = 10000
    
    # Google AI settings
    google_api_key: str
    ai_model: str = "gemini-1.5-flash"
    
    # Redis settings
    redis_url: str = "redis://localhost:6379/0"
    cache_ttl: int = 3600
    
    # Celery settings
    celery_broker_url: str = "redis://localhost:6379/1"
    celery_result_backend: str = "redis://localhost:6379/2"
    
    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()