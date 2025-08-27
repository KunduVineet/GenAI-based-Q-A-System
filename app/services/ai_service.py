import google.generativeai as genai
from typing import Dict, Any, Optional
from app.core.config import settings
from app.models.requests import (
    SummarizeRequest, QuestionAnswerRequest, 
    ToneRewriteRequest, TranslateRequest
)
from app.utils.logger import app_logger
from app.utils.helpers import timing_decorator

class AIService:
    """Google Generative AI service"""
    
    def __init__(self):
        genai.configure(api_key=settings.google_api_key)
        self.model = genai.GenerativeModel(settings.ai_model)
        app_logger.info(f"Initialized AI service with model: {settings.ai_model}")
    
    @timing_decorator
    async def summarize_text(self, request: SummarizeRequest) -> str:
        """Summarize text using AI"""
        prompt = f"""Summarize the following text in approximately {request.max_length} characters.
Focus on the key points and main ideas. Make it concise and clear.

Text to summarize:
{request.text}

Summary:"""
        
        try:
            response = self.model.generate_content(prompt)
            result = response.text.strip()
            app_logger.info(f"Successfully summarized text of {len(request.text)} characters")
            return result
        except Exception as e:
            app_logger.error(f"Error summarizing text: {str(e)}")
            raise Exception(f"AI summarization failed: {str(e)}")
    
    @timing_decorator
    async def answer_question(self, request: QuestionAnswerRequest) -> str:
        """Answer question based on context"""
        prompt = f"""Based on the following context, answer the question accurately and concisely.
If the answer is not available in the context, say so clearly.

Context:
{request.context}

Question: {request.question}

Answer:"""
        
        try:
            response = self.model.generate_content(prompt)
            result = response.text.strip()
            app_logger.info("Successfully answered question")
            return result
        except Exception as e:
            app_logger.error(f"Error answering question: {str(e)}")
            raise Exception(f"AI question answering failed: {str(e)}")
    
    @timing_decorator
    async def rewrite_tone(self, request: ToneRewriteRequest) -> str:
        """Rewrite text with different tone"""
        prompt = f"""Rewrite the following text to match the target tone: {request.target_tone}
Keep the meaning intact while changing the style and tone appropriately.

Original text:
{request.text}

Rewritten text ({request.target_tone} tone):"""
        
        try:
            response = self.model.generate_content(prompt)
            result = response.text.strip()
            app_logger.info(f"Successfully rewrote text to {request.target_tone} tone")
            return result
        except Exception as e:
            app_logger.error(f"Error rewriting tone: {str(e)}")
            raise Exception(f"AI tone rewriting failed: {str(e)}")
    
    @timing_decorator
    async def translate_text(self, request: TranslateRequest) -> str:
        """Translate text to target language"""
        source_lang = f"from {request.source_language} " if request.source_language else ""
        prompt = f"""Translate the following text {source_lang}to {request.target_language}.
Provide only the translation, no explanations.

Text to translate:
{request.text}

Translation:"""
        
        try:
            response = self.model.generate_content(prompt)
            result = response.text.strip()
            app_logger.info(f"Successfully translated text to {request.target_language}")
            return result
        except Exception as e:
            app_logger.error(f"Error translating text: {str(e)}")
            raise Exception(f"AI translation failed: {str(e)}")

ai_service = AIService()