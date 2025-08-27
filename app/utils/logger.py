import sys
from loguru import logger
from app.core.config import settings

def setup_logger():
    """Setup application logger"""
    logger.remove()
    
    log_format = (
        "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
        "<level>{level: <8}</level> | "
        "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
        "<level>{message}</level>"
    )
    
    logger.add(
        sys.stdout,
        format=log_format,
        level="DEBUG" if settings.debug else "INFO",
        colorize=True
    )
    
    logger.add(
        "logs/app.log",
        format=log_format,
        level="INFO",
        rotation="1 day",
        retention="7 days",
        compression="zip"
    )
    
    return logger

app_logger = setup_logger()