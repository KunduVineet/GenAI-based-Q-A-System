import pytest
from fastapi.testclient import TestClient
from app.main import app

@pytest.fixture
def client():
    """Test client fixture"""
    return TestClient(app)

@pytest.fixture
def sample_text():
    """Sample text for testing"""
    return "This is a sample text for testing purposes. It contains multiple sentences and should be long enough to test summarization functionality."

@pytest.fixture
def sample_context():
    """Sample context for Q&A testing"""
    return "Python is a high-level programming language. It was created by Guido van Rossum and released in 1991. Python is known for its simple syntax and readability."