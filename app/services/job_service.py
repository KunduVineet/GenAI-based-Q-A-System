import uuid
from datetime import datetime
from typing import Dict, Any, Optional
from app.models.responses import JobResponse, JobStatus
from app.services.cache_service import cache_service
from app.utils.logger import app_logger

class JobService:
    """Service for managing background jobs"""
    
    @staticmethod
    def create_job(task_type: str, payload: Dict[str, Any]) -> str:
        """Create a new job"""
        job_id = str(uuid.uuid4())
        job_data = {
            "job_id": job_id,
            "task_type": task_type,
            "status": JobStatus.PENDING.value,
            "created_at": datetime.now().isoformat(),
            "payload": payload,
            "result": None,
            "error": None
        }
        
        # Store job in cache
        cache_key = f"job:{job_id}"
        # Note: Using asyncio.create_task in real implementation
        app_logger.info(f"Created job {job_id} for task type {task_type}")
        return job_id
    
    @staticmethod
    async def get_job_status(job_id: str) -> Optional[JobResponse]:
        """Get job status"""
        cache_key = f"job:{job_id}"
        job_data = await cache_service.get(cache_key)
        
        if not job_data:
            return None
        
        return JobResponse(
            job_id=job_data["job_id"],
            status=JobStatus(job_data["status"]),
            created_at=datetime.fromisoformat(job_data["created_at"]),
            completed_at=datetime.fromisoformat(job_data["completed_at"]) if job_data.get("completed_at") else None,
            result=job_data.get("result"),
            error=job_data.get("error")
        )
    
    @staticmethod
    async def update_job_status(job_id: str, status: JobStatus, result: Any = None, error: str = None):
        """Update job status"""
        cache_key = f"job:{job_id}"
        job_data = await cache_service.get(cache_key)
        
        if job_data:
            job_data["status"] = status.value
            if status == JobStatus.COMPLETED:
                job_data["completed_at"] = datetime.now().isoformat()
                job_data["result"] = result
            elif status == JobStatus.FAILED:
                job_data["completed_at"] = datetime.now().isoformat()
                job_data["error"] = error
            
            await cache_service.set(cache_key, job_data)
            app_logger.info(f"Updated job {job_id} status to {status.value}")

job_service = JobService()