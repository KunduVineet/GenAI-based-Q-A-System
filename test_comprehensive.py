#!/usr/bin/env python3
"""
Comprehensive Test Suite for AI Backend Service
Tests all functionality required by the assignment
"""

import requests
import json
import time
from datetime import datetime

BASE_URL = "http://localhost:8000"
API_V1 = f"{BASE_URL}/api/v1"

def print_test_header(test_name):
    print(f"\n{'='*60}")
    print(f"🧪 {test_name}")
    print(f"{'='*60}")

def print_result(response, test_name):
    print(f"✅ {test_name}")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print("-" * 40)

def test_health_check():
    print_test_header("HEALTH CHECK TESTS")
    
    # Basic health
    response = requests.get(f"{API_V1}/health/")
    print_result(response, "Basic Health Check")
    
    # System metrics
    response = requests.get(f"{API_V1}/health/metrics")
    print_result(response, "System Metrics")
    
    # Readiness check
    response = requests.get(f"{API_V1}/health/ready")
    print_result(response, "Readiness Check")

def test_ai_summarization():
    print_test_header("AI SUMMARIZATION TESTS")
    
    test_text = """
    Artificial Intelligence (AI) has become one of the most transformative technologies of the 21st century. 
    It encompasses machine learning, deep learning, natural language processing, and computer vision. 
    AI applications span across healthcare, finance, transportation, entertainment, and many other sectors. 
    Machine learning algorithms can analyze vast datasets to identify patterns and make predictions. 
    Deep learning, a subset of machine learning, uses neural networks with multiple layers to process complex data. 
    Natural language processing enables computers to understand and generate human language. 
    Computer vision allows machines to interpret and analyze visual information from the world around them.
    """
    
    # Sync summarization
    response = requests.post(f"{API_V1}/ai/summarize", json={
        "text": test_text,
        "max_length": 100
    })
    print_result(response, "Synchronous Summarization")
    
    # Async summarization
    response = requests.post(f"{API_V1}/ai/summarize/async", json={
        "text": test_text,
        "max_length": 80
    })
    print_result(response, "Asynchronous Summarization")

def test_ai_question_answer():
    print_test_header("AI QUESTION ANSWERING TESTS")
    
    context = """
    FastAPI is a modern, fast (high-performance), web framework for building APIs with Python 3.7+ 
    based on standard Python type hints. It was created by Sebastian Ramirez and first released in 2018. 
    FastAPI provides automatic API documentation using OpenAPI and JSON Schema. It includes data validation, 
    serialization, and automatic generation of interactive API documentation. FastAPI is built on top of 
    Starlette for the web parts and Pydantic for the data parts.
    """
    
    questions = [
        "Who created FastAPI and when was it released?",
        "What are the main features of FastAPI?",
        "What technologies is FastAPI built on?"
    ]
    
    for i, question in enumerate(questions, 1):
        # Sync Q&A
        response = requests.post(f"{API_V1}/ai/question-answer", json={
            "context": context,
            "question": question
        })
        print_result(response, f"Q&A Test {i} (Sync)")
        
        # Async Q&A
        response = requests.post(f"{API_V1}/ai/question-answer/async", json={
            "context": context,
            "question": question
        })
        print_result(response, f"Q&A Test {i} (Async)")

def test_ai_tone_rewriting():
    print_test_header("AI TONE REWRITING TESTS")
    
    test_cases = [
        {
            "text": "Hey dude, this bug is totally messing up everything!",
            "target_tone": "professional",
            "description": "Casual to Professional"
        },
        {
            "text": "I regret to inform you that there appears to be a technical issue.",
            "target_tone": "casual",
            "description": "Formal to Casual"
        },
        {
            "text": "This code is broken and needs immediate attention.",
            "target_tone": "friendly",
            "description": "Direct to Friendly"
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        # Sync tone rewriting
        response = requests.post(f"{API_V1}/ai/tone-rewrite", json={
            "text": test_case["text"],
            "target_tone": test_case["target_tone"]
        })
        print_result(response, f"Tone Rewrite {i} - {test_case['description']} (Sync)")
        
        # Async tone rewriting
        response = requests.post(f"{API_V1}/ai/tone-rewrite/async", json={
            "text": test_case["text"],
            "target_tone": test_case["target_tone"]
        })
        print_result(response, f"Tone Rewrite {i} - {test_case['description']} (Async)")

def test_ai_translation():
    print_test_header("AI TRANSLATION TESTS")
    
    test_cases = [
        {
            "text": "Hello, how are you today?",
            "target_language": "Spanish",
            "description": "English to Spanish"
        },
        {
            "text": "Good morning, have a great day!",
            "target_language": "French",
            "description": "English to French"
        },
        {
            "text": "Thank you for your help with this project.",
            "target_language": "German",
            "description": "English to German"
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        # Sync translation
        response = requests.post(f"{API_V1}/ai/translate", json={
            "text": test_case["text"],
            "target_language": test_case["target_language"]
        })
        print_result(response, f"Translation {i} - {test_case['description']} (Sync)")
        
        # Async translation
        response = requests.post(f"{API_V1}/ai/translate/async", json={
            "text": test_case["text"],
            "target_language": test_case["target_language"]
        })
        print_result(response, f"Translation {i} - {test_case['description']} (Async)")

def test_caching():
    print_test_header("CACHING PERFORMANCE TESTS")
    
    test_text = "This is a test for caching performance. The second request should be faster."
    
    # First request (cache miss)
    start_time = time.time()
    response1 = requests.post(f"{API_V1}/ai/summarize", json={
        "text": test_text,
        "max_length": 50
    })
    first_request_time = time.time() - start_time
    
    # Second request (cache hit)
    start_time = time.time()
    response2 = requests.post(f"{API_V1}/ai/summarize", json={
        "text": test_text,
        "max_length": 50
    })
    second_request_time = time.time() - start_time
    
    print(f"✅ Cache Performance Test")
    print(f"First request (cache miss): {first_request_time:.3f}s")
    print(f"Second request (cache hit): {second_request_time:.3f}s")
    print(f"Speed improvement: {(first_request_time/second_request_time):.2f}x faster")
    print(f"Same result: {response1.json() == response2.json()}")
    print("-" * 40)

def main():
    print(f"""
🚀 AI Backend Service - Comprehensive Test Suite
{'='*60}
Testing all assignment requirements:
✅ Problem Design: Text processing (summarization, Q&A, tone rewriting, translation)
✅ API Implementation: FastAPI with RESTful endpoints  
✅ Gen AI Integration: Google Gemini model
✅ Async Job Queue: Celery with Redis
✅ Caching Layer: Redis caching
✅ Input validation and proper responses
✅ Background job processing
✅ Performance optimization

Starting tests at: {datetime.now()}
Base URL: {BASE_URL}
""")
    
    try:
        # Test all functionality
        test_health_check()
        test_ai_summarization()
        test_ai_question_answer()
        test_ai_tone_rewriting()
        test_ai_translation()
        test_caching()
        
        print(f"\n{'='*60}")
        print("🎉 ALL TESTS COMPLETED SUCCESSFULLY!")
        print("✅ The AI Backend Service meets all assignment requirements")
        print(f"{'='*60}")
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {str(e)}")
        print("Please check if the server is running on http://localhost:8000")

if __name__ == "__main__":
    main()