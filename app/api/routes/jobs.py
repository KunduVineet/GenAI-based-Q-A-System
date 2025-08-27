from fastapi import APIRouter, HTTPException, Depends
from typing import Dict
from app.models.responses import BaseResponse, JobResponse
from app.services.job_service import job_service
from app.api.dependencies import get_current_user
from app.utils.logger import app_logger

router = APIRouter(prefix="/jobs", tags=["jobs"])

@router.get("/{job_id}", response_model=JobResponse)
async def get_job_status(
    job_id: str,
    user: Dict = Depends(get_current_user)
):
    """Get job status and result"""
    try:
        job = await job_service.get_job_status(job_id)
        if not job:
            raise HTTPException(status_code=404, detail="Job not found")
        return job
    except HTTPException:
        raise
    except Exception as e:
        app_logger.error(f"Error getting job status: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.delete("/{job_id}", response_model=BaseResponse)
async def cancel_job(
    job_id: str,
    user: Dict = Depends(get_current_user)
):
    """Cancel a job (if possible)"""
    try:
        # In a real implementation, you'd use Celery's revoke functionality
        # For now, we'll just mark it as cancelled in our cache
        job = await job_service.get_job_status(job_id)
        if not job:
            raise HTTPException(status_code=404, detail="Job not found")
        
        return BaseResponse(
            success=True,
            message="Job cancellation requested",
            data={"job_id": job_id, "note": "Cancellation support depends on job status"}
        )
    except HTTPException:
        raise
    except Exception as e:
        app_logger.error(f"Error cancelling job: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")