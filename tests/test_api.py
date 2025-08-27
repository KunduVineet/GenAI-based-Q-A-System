import pytest
from fastapi.testclient import TestClient

def test_root_endpoint(client):
    """Test root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "version" in data

def test_health_check(client):
    """Test health check endpoint"""
    response = client.get("/api/v1/health/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "services" in data

def test_summarize_endpoint(client, sample_text):
    """Test summarization endpoint"""
    payload = {
        "text": sample_text,
        "max_length": 100
    }
    response = client.post("/api/v1/ai/summarize", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "summary" in data["data"]

def test_question_answer_endpoint(client, sample_context):
    """Test question answering endpoint"""
    payload = {
        "context": sample_context,
        "question": "Who created Python?"
    }
    response = client.post("/api/v1/ai/question-answer", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "answer" in data["data"]

def test_async_summarize_endpoint(client, sample_text):
    """Test async summarization endpoint"""
    payload = {
        "text": sample_text,
        "max_length": 100
    }
    response = client.post("/api/v1/ai/summarize/async", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "job_id" in data["data"]

def test_invalid_input_validation(client):
    """Test input validation"""
    payload = {
        "text": "",  # Empty text should fail validation
        "max_length": 100
    }
    response = client.post("/api/v1/ai/summarize", json=payload)
    assert response.status_code == 422  # Validation error