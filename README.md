# AI Backend Service

A production-ready backend service that integrates Google's Generative AI (Gemini) for various text processing tasks including summarization, question answering, tone rewriting, and translation. Built with FastAPI, Celery, and Redis for scalability and performance.

## Features

- **AI-Powered Text Processing**: Summarization, Q&A, tone rewriting, and translation using Google's Gemini AI
- **Synchronous & Asynchronous Processing**: Support for both immediate and background job processing
- **Intelligent Caching**: Redis-based caching to improve response times and reduce AI API costs
- **Scalable Architecture**: Designed to handle thousands of requests per day
- **Comprehensive API**: RESTful APIs with proper validation and error handling
- **Production Ready**: Docker containerization, health checks, monitoring, and deployment configs
- **Background Jobs**: Celery-based async task processing with job status tracking

## Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   FastAPI App   │    │   Redis Cache   │    │  Google AI API  │
│                 │◄──►│                 │    │    (Gemini)     │
│  - REST API     │    │  - Caching      │    │                 │
│  - Validation   │    │  - Job Queue    │    │  - Summarization│
│  - Middleware   │    │                 │    │  - Q&A          │
└─────────────────┘    └─────────────────┘    │  - Translation  │
│                       │                     │  - Tone Rewrite │
│                       │                     └─────────────────┘
▼                       ▼
┌─────────────────┐    ┌─────────────────┐
│ Celery Workers  │    │   Job Service   │
│                 │    │                 │
│ - Background    │◄──►│ - Status Track  │
│   Processing    │    │ - Result Store  │
│ - Async Tasks   │    │                 │
└─────────────────┘    └─────────────────┘
```

## Quick Start

### Prerequisites
- Python 3.11+
- Redis server
- Google AI API key

### Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd ai-backend-service
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Environment setup**
```bash
cp .env.example .env
# Edit .env with your Google API key and other settings
```

4. **Start Redis** (if not using Docker)
```bash
redis-server
```

5. **Run the application**
```bash
# Start FastAPI server
uvicorn app.main:app --reload

# In another terminal, start Celery worker
celery -A app.workers.celery_worker worker --loglevel=info
```

### Using Docker

```bash
# Build and start all services
docker-compose -f docker/docker-compose.yml up --build

# Access the API at http://localhost:8000
# API documentation at http://localhost:8000/docs
# Celery monitoring at http://localhost:5555
```

## API Reference

### Base URL
```
http://localhost:8000/api/v1
```

### Authentication
Currently, the API uses optional authentication. In production, implement proper API key validation.

### Endpoints

#### Health Check
```http
GET /health/
```

#### Text Summarization
```http
# Synchronous
POST /ai/summarize
{
  "text": "Your long text here...",
  "max_length": 200
}

# Asynchronous
POST /ai/summarize/async
{
  "text": "Your long text here...",
  "max_length": 200
}
```

#### Question Answering
```http
# Synchronous
POST /ai/question-answer
{
  "context": "Python is a programming language...",
  "question": "What is Python?"
}

# Asynchronous
POST /ai/question-answer/async
{
  "context": "Context text...",
  "question": "Your question?"
}
```

#### Tone Rewriting
```http
# Synchronous
POST /ai/tone-rewrite
{
  "text": "Your text here",
  "target_tone": "formal"
}

# Asynchronous
POST /ai/tone-rewrite/async
{
  "text": "Your text here",
  "target_tone": "professional"
}
```

#### Translation
```http
# Synchronous
POST /ai/translate
{
  "text": "Hello world",
  "target_language": "Spanish",
  "source_language": "English"  // optional
}

# Asynchronous
POST /ai/translate/async
{
  "text": "Hello world",
  "target_language": "French"
}
```

#### Job Status
```http
GET /jobs/{job_id}
DELETE /jobs/{job_id}
```

## Example Usage

### Python Client Example
```python
import requests

# Synchronous summarization
response = requests.post(
    "http://localhost:8000/api/v1/ai/summarize",
    json={
        "text": "Your long article text here...",
        "max_length": 150
    }
)
result = response.json()
print(result["data"]["summary"])

# Asynchronous processing
async_response = requests.post(
    "http://localhost:8000/api/v1/ai/summarize/async",
    json={"text": "Long text...", "max_length": 150}
)
job_id = async_response.json()["data"]["job_id"]

# Check job status
status_response = requests.get(f"http://localhost:8000/api/v1/jobs/{job_id}")
job_status = status_response.json()
```

### JavaScript/Node.js Example
```javascript
// Synchronous request
const response = await fetch('http://localhost:8000/api/v1/ai/summarize', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    text: "Your text to summarize...",
    max_length: 100
  })
});

const result = await response.json();
console.log(result.data.summary);
```

### cURL Example
```bash
# Summarize text
curl -X POST "http://localhost:8000/api/v1/ai/summarize" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Artificial Intelligence is transforming industries...",
    "max_length": 100
  }'

# Question answering
curl -X POST "http://localhost:8000/api/v1/ai/question-answer" \
  -H "Content-Type: application/json" \
  -d '{
    "context": "FastAPI is a modern web framework for building APIs",
    "question": "What is FastAPI?"
  }'
```

## Caching Strategy

The service implements intelligent caching to optimize performance:

1. **Cache Key Generation**: MD5 hash of input content + parameters
2. **Cache TTL**: Configurable (default: 1 hour)
3. **Cache Levels**:
   - Summarization: `summary:{content_hash}_{max_length}`
   - Q&A: `qa:{context_hash}_{question_hash}`
   - Translation: `translate:{text_hash}_{target_lang}_{source_lang}`
   - Tone rewriting: `tone:{text_hash}_{target_tone}`
4. **Cache Invalidation**: TTL-based automatic expiration
5. **Cache Hits**: Logged for monitoring and optimization

## Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `GOOGLE_API_KEY` | Google AI API key | Required |
| `REDIS_URL` | Redis connection URL | `redis://localhost:6379/0` |
| `CELERY_BROKER_URL` | Celery broker URL | `redis://localhost:6379/1` |
| `CELERY_RESULT_BACKEND` | Celery results backend | `redis://localhost:6379/2` |
| `DEBUG` | Debug mode | `false` |
| `AI_MODEL` | Google AI model | `gemini-1.5-flash` |
| `CACHE_TTL` | Cache TTL in seconds | `3600` |
| `MAX_REQUEST_SIZE` | Max request size | `10000` |

### Model Configuration

The service uses Google's Gemini 1.5 Flash model by default. You can configure this by setting the `AI_MODEL` environment variable to other available models:

- `gemini-1.5-flash` (default - fast and efficient)
- `gemini-1.5-pro` (more capable, slower)
- `gemini-pro` (legacy model)

## Deployment

### Render.com Deployment
1. Connect your repository to Render
2. Use the provided `deployment/render.yaml` configuration
3. Set environment variables in Render dashboard
4. Deploy with automatic Redis and worker services

### Fly.io Deployment
```bash
# Install flyctl
curl -L https://fly.io/install.sh | sh

# Login and deploy
fly auth login
fly launch
fly deploy
```

### Manual Deployment
1. Set up Redis server
2. Configure environment variables
3. Run database migrations (if any)
4. Start services:
```bash
# API server
gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app

# Celery worker
celery -A app.workers.celery_worker worker --loglevel=info
```

## Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app

# Run specific test file
pytest tests/test_api.py
```

## Monitoring

- **Health Checks**: `/api/v1/health/` endpoint
- **Metrics**: Built-in request timing middleware
- **Logging**: Structured logging with Loguru
- **Celery Monitoring**: Flower web interface at port 5555

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request
