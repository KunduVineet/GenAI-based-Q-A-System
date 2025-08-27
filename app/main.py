from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
import time
import os

from app.core.config import settings
from app.api.routes import health, ai_tasks, jobs
from app.utils.logger import app_logger

# Create logs directory
os.makedirs("logs", exist_ok=True)

# Create FastAPI app
app = FastAPI(
    title=settings.app_name,
    version=settings.version,
    description="AI Backend Service with Generative AI Integration",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["*"]  # Configure appropriately for production
)

# Add request timing middleware
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response

# Exception handlers
@app.exception_handler(404)
async def not_found_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=404,
        content={"success": False, "message": "Endpoint not found", "data": None}
    )

@app.exception_handler(500)
async def internal_error_handler(request: Request, exc: Exception):
    app_logger.error(f"Internal server error: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"success": False, "message": "Internal server error", "data": None}
    )

# Include routers
app.include_router(health.router, prefix=settings.api_v1_prefix)
app.include_router(ai_tasks.router, prefix=settings.api_v1_prefix)
app.include_router(jobs.router, prefix=settings.api_v1_prefix)

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": f"Welcome to {settings.app_name}",
        "version": settings.version,
        "docs": "/docs",
        "health": f"{settings.api_v1_prefix}/health"
    }

# Startup and shutdown events
@app.on_event("startup")
async def startup_event():
    """Application startup"""
    app_logger.info(f"Starting {settings.app_name} v{settings.version}")
    app_logger.info(f"Debug mode: {settings.debug}")

@app.on_event("shutdown")
async def shutdown_event():
    """Application shutdown"""
    app_logger.info(f"Shutting down {settings.app_name}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug
    )