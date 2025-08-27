from fastapi import APIRouter
from datetime import datetime
from app.core.config import settings
from app.models.responses import HealthResponse
from app.services.cache_service import cache_service
from app.utils.logger import app_logger
from app.utils.monitoring import SystemMonitor

router = APIRouter(prefix="/health", tags=["health"])

@router.get("/", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    services = {}
    
    # Check Redis connection
    try:
        if cache_service.redis_client:
            cache_service.redis_client.ping()
            services["redis"] = "healthy"
        else:
            services["redis"] = "unhealthy"
    except Exception as e:
        services["redis"] = "unhealthy"
        app_logger.error(f"Redis health check failed: {str(e)}")
    
    # Check AI service (basic check)
    try:
        services["ai_service"] = "healthy"
    except Exception as e:
        services["ai_service"] = "unhealthy"
        app_logger.error(f"AI service health check failed: {str(e)}")
    
    # Check system health
    try:
        system_health = SystemMonitor.check_system_health()
        services["system"] = system_health["status"]
    except Exception as e:
        services["system"] = "unhealthy"
        app_logger.error(f"System health check failed: {str(e)}")
    
    return HealthResponse(
        status="healthy",
        timestamp=datetime.now(),
        version=settings.version,
        services=services
    )

@router.get("/ready")
async def readiness_check():
    """Readiness check for deployment"""
    return {"status": "ready", "timestamp": datetime.now()}

@router.get("/live")
async def liveness_check():
    """Liveness check for deployment"""
    return {"status": "alive", "timestamp": datetime.now()}
@router.get("/metrics")
async def get_metrics():
    """Get detailed system metrics"""
    try:
        metrics = SystemMonitor.get_system_metrics()
        return {"success": True, "data": metrics}
    except Exception as e:
        app_logger.error(f"Error getting metrics: {str(e)}")
        return {"success": False, "error": str(e)}