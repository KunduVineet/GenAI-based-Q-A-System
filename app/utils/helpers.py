import time
import asyncio
from functools import wraps
from typing import Callable, Any
from app.utils.logger import app_logger

def timing_decorator(func: Callable) -> Callable:
    """Decorator to measure function execution time"""
    if asyncio.iscoroutinefunction(func):
        @wraps(func)
        async def async_wrapper(*args, **kwargs) -> Any:
            start_time = time.time()
            result = await func(*args, **kwargs)
            execution_time = time.time() - start_time
            app_logger.info(f"{func.__name__} executed in {execution_time:.4f} seconds")
            return result
        return async_wrapper
    else:
        @wraps(func)
        def sync_wrapper(*args, **kwargs) -> Any:
            start_time = time.time()
            result = func(*args, **kwargs)
            execution_time = time.time() - start_time
            app_logger.info(f"{func.__name__} executed in {execution_time:.4f} seconds")
            return result
        return sync_wrapper

def truncate_text(text: str, max_length: int = 100) -> str:
    """Truncate text for logging"""
    if len(text) <= max_length:
        return text
    return text[:max_length] + "..."