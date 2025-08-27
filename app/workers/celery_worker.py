import asyncio
from celery import Celery
from app.core.config import settings
from app.services.ai_service import ai_service
from app.services.job_service import job_service
from app.models.requests import (
    SummarizeRequest, QuestionAnswerRequest,
    ToneRewriteRequest, TranslateRequest
)
from app.models.responses import JobStatus
from app.utils.logger import app_logger

# Create Celery app
celery_app = Celery(
    "ai_backend_worker",
    broker=settings.celery_broker_url,
    backend=settings.celery_result_backend,
    include=["app.workers.celery_worker"]
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=300,  # 5 minutes
    task_soft_time_limit=240,  # 4 minutes
)

@celery_app.task(bind=True, name="process_summarize_task")
def process_summarize_task(self, job_id: str, payload: dict):
    """Process text summarization task"""
    async def _process():
        try:
            await job_service.update_job_status(job_id, JobStatus.PROCESSING)
            request = SummarizeRequest(**payload)
            result = await ai_service.summarize_text(request)
            await job_service.update_job_status(
                job_id, JobStatus.COMPLETED, 
                {"summary": result, "task_type": "summarize"}
            )
            app_logger.info(f"Completed summarize task for job {job_id}")
            return result
        except Exception as e:
            error_msg = str(e)
            await job_service.update_job_status(job_id, JobStatus.FAILED, error=error_msg)
            app_logger.error(f"Failed summarize task for job {job_id}: {error_msg}")
            raise
    
    # Run async function in sync context
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        return loop.run_until_complete(_process())
    finally:
        loop.close()

@celery_app.task(bind=True, name="process_question_answer_task")
def process_question_answer_task(self, job_id: str, payload: dict):
    """Process question answering task"""
    async def _process():
        try:
            await job_service.update_job_status(job_id, JobStatus.PROCESSING)
            request = QuestionAnswerRequest(**payload)
            result = await ai_service.answer_question(request)
            await job_service.update_job_status(
                job_id, JobStatus.COMPLETED, 
                {"answer": result, "task_type": "question_answer"}
            )
            app_logger.info(f"Completed Q&A task for job {job_id}")
            return result
        except Exception as e:
            error_msg = str(e)
            await job_service.update_job_status(job_id, JobStatus.FAILED, error=error_msg)
            app_logger.error(f"Failed Q&A task for job {job_id}: {error_msg}")
            raise
    
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        return loop.run_until_complete(_process())
    finally:
        loop.close()

@celery_app.task(bind=True, name="process_tone_rewrite_task")
def process_tone_rewrite_task(self, job_id: str, payload: dict):
    """Process tone rewriting task"""
    async def _process():
        try:
            await job_service.update_job_status(job_id, JobStatus.PROCESSING)
            request = ToneRewriteRequest(**payload)
            result = await ai_service.rewrite_tone(request)
            await job_service.update_job_status(
                job_id, JobStatus.COMPLETED, 
                {"rewritten_text": result, "task_type": "tone_rewrite"}
            )
            app_logger.info(f"Completed tone rewrite task for job {job_id}")
            return result
        except Exception as e:
            error_msg = str(e)
            await job_service.update_job_status(job_id, JobStatus.FAILED, error=error_msg)
            app_logger.error(f"Failed tone rewrite task for job {job_id}: {error_msg}")
            raise
    
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        return loop.run_until_complete(_process())
    finally:
        loop.close()

@celery_app.task(bind=True, name="process_translate_task")
def process_translate_task(self, job_id: str, payload: dict):
    """Process translation task"""
    async def _process():
        try:
            await job_service.update_job_status(job_id, JobStatus.PROCESSING)
            request = TranslateRequest(**payload)
            result = await ai_service.translate_text(request)
            await job_service.update_job_status(
                job_id, JobStatus.COMPLETED, 
                {"translation": result, "task_type": "translate"}
            )
            app_logger.info(f"Completed translation task for job {job_id}")
            return result
        except Exception as e:
            error_msg = str(e)
            await job_service.update_job_status(job_id, JobStatus.FAILED, error=error_msg)
            app_logger.error(f"Failed translation task for job {job_id}: {error_msg}")
            raise
    
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        return loop.run_until_complete(_process())
    finally:
        loop.close()