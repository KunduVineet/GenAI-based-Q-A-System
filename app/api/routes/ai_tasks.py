from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from typing import Dict, Any
from app.models.requests import (
    SummarizeRequest, QuestionAnswerRequest,
    ToneRewriteRequest, TranslateRequest
)
from app.models.responses import BaseResponse, AITaskResponse
from app.services.ai_service import ai_service
from app.services.cache_service import cache_service
from app.services.job_service import job_service
from app.workers.celery_worker import (
    process_summarize_task, process_question_answer_task,
    process_tone_rewrite_task, process_translate_task
)
from app.api.dependencies import get_current_user, validate_request_size
from app.utils.logger import app_logger
import time

router = APIRouter(prefix="/ai", tags=["ai"])

@router.post("/summarize", response_model=BaseResponse)
async def summarize_text_sync(
    request: SummarizeRequest,
    user: Dict = Depends(get_current_user),
    _: None = Depends(validate_request_size)
):
    """Synchronously summarize text"""
    try:
        # Check cache first
        cache_key = cache_service.create_key("summary", f"{request.text}_{request.max_length}")
        cached_result = await cache_service.get(cache_key)
        
        if cached_result:
            app_logger.info("Returning cached summary")
            return BaseResponse(
                success=True,
                message="Text summarized successfully (cached)",
                data={"summary": cached_result["summary"], "cached": True}
            )
        
        # Generate summary
        start_time = time.time()
        summary = await ai_service.summarize_text(request)
        processing_time = time.time() - start_time
        
        # Cache result
        result_data = {"summary": summary, "processing_time": processing_time}
        await cache_service.set(cache_key, result_data)
        
        return BaseResponse(
            success=True,
            message="Text summarized successfully",
            data={**result_data, "cached": False}
        )
    except Exception as e:
        app_logger.error(f"Error in summarize endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/summarize/async", response_model=BaseResponse)
async def summarize_text_async(
    request: SummarizeRequest,
    user: Dict = Depends(get_current_user)
):
    """Asynchronously summarize text"""
    try:
        # Create job
        job_id = job_service.create_job("summarize", request.dict())
        
        # Queue task
        process_summarize_task.delay(job_id, request.dict())
        
        return BaseResponse(
            success=True,
            message="Summarization task queued successfully",
            data={"job_id": job_id}
        )
    except Exception as e:
        app_logger.error(f"Error in async summarize endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/question-answer", response_model=BaseResponse)
async def answer_question_sync(
    request: QuestionAnswerRequest,
    user: Dict = Depends(get_current_user)
):
    """Synchronously answer question"""
    try:
        # Check cache
        cache_key = cache_service.create_key("qa", f"{request.context}_{request.question}")
        cached_result = await cache_service.get(cache_key)
        
        if cached_result:
            return BaseResponse(
                success=True,
                message="Question answered successfully (cached)",
                data={"answer": cached_result["answer"], "cached": True}
            )
        
        # Generate answer
        start_time = time.time()
        answer = await ai_service.answer_question(request)
        processing_time = time.time() - start_time
        
        # Cache result
        result_data = {"answer": answer, "processing_time": processing_time}
        await cache_service.set(cache_key, result_data)
        
        return BaseResponse(
            success=True,
            message="Question answered successfully",
            data={**result_data, "cached": False}
        )
    except Exception as e:
        app_logger.error(f"Error in question-answer endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/question-answer/async", response_model=BaseResponse)
async def answer_question_async(
    request: QuestionAnswerRequest,
    user: Dict = Depends(get_current_user)
):
    """Asynchronously answer question"""
    try:
        job_id = job_service.create_job("question_answer", request.dict())
        process_question_answer_task.delay(job_id, request.dict())
        
        return BaseResponse(
            success=True,
            message="Question answering task queued successfully",
            data={"job_id": job_id}
        )
    except Exception as e:
        app_logger.error(f"Error in async question-answer endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/tone-rewrite", response_model=BaseResponse)
async def rewrite_tone_sync(
    request: ToneRewriteRequest,
    user: Dict = Depends(get_current_user)
):
    """Synchronously rewrite text tone"""
    try:
        cache_key = cache_service.create_key("tone", f"{request.text}_{request.target_tone}")
        cached_result = await cache_service.get(cache_key)
        
        if cached_result:
            return BaseResponse(
                success=True,
                message="Text tone rewritten successfully (cached)",
                data={"rewritten_text": cached_result["rewritten_text"], "cached": True}
            )
        
        start_time = time.time()
        rewritten_text = await ai_service.rewrite_tone(request)
        processing_time = time.time() - start_time
        
        result_data = {"rewritten_text": rewritten_text, "processing_time": processing_time}
        await cache_service.set(cache_key, result_data)
        
        return BaseResponse(
            success=True,
            message="Text tone rewritten successfully",
            data={**result_data, "cached": False}
        )
    except Exception as e:
        app_logger.error(f"Error in tone-rewrite endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/tone-rewrite/async", response_model=BaseResponse)
async def rewrite_tone_async(
    request: ToneRewriteRequest,
    user: Dict = Depends(get_current_user)
):
    """Asynchronously rewrite text tone"""
    try:
        job_id = job_service.create_job("tone_rewrite", request.dict())
        process_tone_rewrite_task.delay(job_id, request.dict())
        
        return BaseResponse(
            success=True,
            message="Tone rewriting task queued successfully",
            data={"job_id": job_id}
        )
    except Exception as e:
        app_logger.error(f"Error in async tone-rewrite endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/translate", response_model=BaseResponse)
async def translate_text_sync(
    request: TranslateRequest,
    user: Dict = Depends(get_current_user)
):
    """Synchronously translate text"""
    try:
        cache_key = cache_service.create_key(
            "translate", 
            f"{request.text}_{request.target_language}_{request.source_language}"
        )
        cached_result = await cache_service.get(cache_key)
        
        if cached_result:
            return BaseResponse(
                success=True,
                message="Text translated successfully (cached)",
                data={"translation": cached_result["translation"], "cached": True}
            )
        
        start_time = time.time()
        translation = await ai_service.translate_text(request)
        processing_time = time.time() - start_time
        
        result_data = {"translation": translation, "processing_time": processing_time}
        await cache_service.set(cache_key, result_data)
        
        return BaseResponse(
            success=True,
            message="Text translated successfully",
            data={**result_data, "cached": False}
        )
    except Exception as e:
        app_logger.error(f"Error in translate endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/translate/async", response_model=BaseResponse)
async def translate_text_async(
    request: TranslateRequest,
    user: Dict = Depends(get_current_user)
):
    """Asynchronously translate text"""
    try:
        job_id = job_service.create_job("translate", request.dict())
        process_translate_task.delay(job_id, request.dict())
        
        return BaseResponse(
            success=True,
            message="Translation task queued successfully",
            data={"job_id": job_id}
        )
    except Exception as e:
        app_logger.error(f"Error in async translate endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))