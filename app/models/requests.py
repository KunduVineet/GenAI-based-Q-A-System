from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from enum import Enum

class AITaskType(str, Enum):
    SUMMARIZE = "summarize"
    QUESTION_ANSWER = "question_answer"
    TONE_REWRITE = "tone_rewrite"
    TRANSLATE = "translate"

class SummarizeRequest(BaseModel):
    text: str = Field(..., min_length=10, max_length=10000, description="Text to summarize")
    max_length: Optional[int] = Field(200, ge=50, le=1000, description="Maximum summary length")

class QuestionAnswerRequest(BaseModel):
    context: str = Field(..., min_length=10, max_length=5000, description="Context for answering")
    question: str = Field(..., min_length=5, max_length=500, description="Question to answer")

class ToneRewriteRequest(BaseModel):
    text: str = Field(..., min_length=5, max_length=2000, description="Text to rewrite")
    target_tone: str = Field(..., min_length=3, max_length=50, description="Target tone (e.g., formal, casual, professional)")

class TranslateRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=2000, description="Text to translate")
    target_language: str = Field(..., min_length=2, max_length=20, description="Target language")
    source_language: Optional[str] = Field(None, min_length=2, max_length=20, description="Source language (auto-detect if not provided)")