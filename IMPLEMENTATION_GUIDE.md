# Complete Implementation Guide

This guide provides step-by-step instructions to implement and run the AI Backend Service with full functionality.

## 🚀 Quick Start (5 Minutes)

### Step 1: Prerequisites Check
Ensure you have:
- Python 3.11+ installed
- Redis server available
- Google AI API key (get from [Google AI Studio](https://makersuite.google.com/app/apikey))

### Step 2: Clone and Setup
```bash
# Clone the repository
git clone <your-repository-url>
cd ai-backend-service

# Make scripts executable (Linux/Mac)
chmod +x scripts/*.sh

# Run automated setup
./scripts/setup.sh
```

### Step 3: Configure Environment
```bash
# Edit the .env file
nano .env  # or use your preferred editor

# Add your Google API key:
GOOGLE_API_KEY=your_actual_api_key_here
```

### Step 4: Start Services
```bash
# Terminal 1: Start Redis
redis-server

# Terminal 2: Start API Server
./scripts/start.sh

# Terminal 3: Start Celery Worker
./scripts/start-worker.sh
```

### Step 5: Test the Service
```bash
# Run the demo client
python examples/client_demo.py

# Or visit the API docs
# Open http://localhost:8000/docs in your browser
```

## 📋 Detailed Implementation Steps

### 1. Environment Setup

#### Option A: Automated Setup (Recommended)
```bash
# Run the setup script
./scripts/setup.sh

# This will:
# - Create virtual environment
# - Install dependencies
# - Create .env file
# - Set up directories
```

#### Option B: Manual Setup
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# Linux/Mac:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# Upgrade pip
pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt

# Create environment file
cp .env.example .env
```

### 2. Configuration

#### Edit .env File
```bash
# Required settings
GOOGLE_API_KEY=your_google_api_key_here

# Optional settings (defaults are fine for development)
DEBUG=true
REDIS_URL=redis://localhost:6379/0
CELERY_BROKER_URL=redis://localhost:6379/1
CELERY_RESULT_BACKEND=redis://localhost:6379/2
AI_MODEL=gemini-1.5-flash
CACHE_TTL=3600
MAX_REQUEST_SIZE=10000
```

#### Get Google AI API Key
1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the key and add it to your .env file

### 3. Start Redis Server

#### Option A: Local Redis Installation
```bash
# Install Redis (Ubuntu/Debian)
sudo apt update
sudo apt install redis-server

# Install Redis (macOS with Homebrew)
brew install redis

# Install Redis (Windows)
# Download from https://redis.io/download

# Start Redis
redis-server
```

#### Option B: Docker Redis
```bash
# Run Redis in Docker
docker run -d --name redis -p 6379:6379 redis:7-alpine
```

#### Option C: Cloud Redis
Use a cloud Redis service like:
- Redis Cloud
- AWS ElastiCache
- Google Cloud Memorystore
- Azure Cache for Redis

Update REDIS_URL in .env accordingly.

### 4. Start the Application

#### Method 1: Using Scripts (Recommended)
```bash
# Terminal 1: API Server
./scripts/start.sh

# Terminal 2: Celery Worker
./scripts/start-worker.sh
```

#### Method 2: Manual Start
```bash
# Terminal 1: API Server
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

# Terminal 2: Celery Worker
celery -A app.workers.celery_worker worker --loglevel=info --concurrency=2

# Terminal 3: Celery Flower (optional monitoring)
celery -A app.workers.celery_worker flower --port=5555
```

#### Method 3: Docker Compose
```bash
# Create .env file first, then:
docker-compose -f docker/docker-compose.yml up --build
```

### 5. Verify Installation

#### Check Service Health
```bash
# Health check
curl http://localhost:8000/api/v1/health/

# System metrics
curl http://localhost:8000/api/v1/health/metrics

# API documentation
# Open http://localhost:8000/docs
```

#### Run Demo Client
```bash
# Run the comprehensive demo
python examples/client_demo.py
```

#### Manual API Testing
```bash
# Test summarization
curl -X POST "http://localhost:8000/api/v1/ai/summarize" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Artificial Intelligence is transforming industries worldwide. Machine learning algorithms can process vast amounts of data to identify patterns and make predictions. As AI continues to evolve, it will create new opportunities and challenges for businesses.",
    "max_length": 100
  }'

# Test question answering
curl -X POST "http://localhost:8000/api/v1/ai/question-answer" \
  -H "Content-Type: application/json" \
  -d '{
    "context": "Python is a programming language created by Guido van Rossum in 1991.",
    "question": "Who created Python?"
  }'
```

## 🔧 Advanced Configuration

### Performance Tuning

#### API Server Optimization
```bash
# Production server with Gunicorn
gunicorn -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000 app.main:app

# Adjust worker count based on CPU cores
# Formula: (2 x CPU cores) + 1
```

#### Celery Worker Optimization
```bash
# Adjust concurrency based on workload
celery -A app.workers.celery_worker worker --loglevel=info --concurrency=4

# Use different queues for different task types
celery -A app.workers.celery_worker worker -Q summarize,translate --loglevel=info
```

#### Redis Optimization
```bash
# Redis configuration for production
# Add to redis.conf:
maxmemory 2gb
maxmemory-policy allkeys-lru
save 900 1
save 300 10
save 60 10000
```

### Monitoring Setup

#### Application Monitoring
```python
# Add to your monitoring system
import requests

def check_service_health():
    try:
        response = requests.get("http://localhost:8000/api/v1/health/")
        return response.json()
    except Exception as e:
        return {"error": str(e)}
```

#### Log Monitoring
```bash
# Monitor application logs
tail -f logs/app.log

# Monitor system logs
sudo journalctl -u ai-backend-api -f
sudo journalctl -u ai-backend-worker -f
```

### Security Configuration

#### API Key Authentication (Optional)
```python
# Add to app/core/security.py
def validate_api_key(api_key: str) -> bool:
    # Implement your API key validation logic
    valid_keys = ["your-secret-api-key"]
    return api_key in valid_keys
```

#### CORS Configuration
```python
# Update app/main.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],  # Specific domains
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)
```

## 🐳 Docker Implementation

### Development with Docker
```bash
# Build and run with Docker Compose
docker-compose -f docker/docker-compose.yml up --build

# Run in background
docker-compose -f docker/docker-compose.yml up -d

# View logs
docker-compose -f docker/docker-compose.yml logs -f api
docker-compose -f docker/docker-compose.yml logs -f worker

# Stop services
docker-compose -f docker/docker-compose.yml down
```

### Production Docker Setup
```bash
# Build production image
docker build -f docker/Dockerfile -t ai-backend-service:prod .

# Run with production environment
docker run -d \
  --name ai-backend-api \
  --env-file .env \
  -p 8000:8000 \
  ai-backend-service:prod

# Run worker
docker run -d \
  --name ai-backend-worker \
  --env-file .env \
  ai-backend-service:prod \
  celery -A app.workers.celery_worker worker --loglevel=info
```

## 🧪 Testing Implementation

### Run Tests
```bash
# Run all tests
./scripts/test.sh

# Or manually:
pytest --cov=app --cov-report=html

# Run specific tests
pytest tests/test_api.py -v
pytest tests/test_services.py -v
```

### Load Testing
```bash
# Install load testing tools
pip install locust

# Create load test file
cat > locustfile.py << EOF
from locust import HttpUser, task, between

class AIServiceUser(HttpUser):
    wait_time = between(1, 3)
    
    @task
    def test_summarize(self):
        self.client.post("/api/v1/ai/summarize", json={
            "text": "This is a test text for summarization.",
            "max_length": 50
        })
    
    @task
    def test_health(self):
        self.client.get("/api/v1/health/")
EOF

# Run load test
locust -f locustfile.py --host=http://localhost:8000
```

## 🚀 Production Deployment

### Server Requirements
- **Minimum**: 2 CPU cores, 4GB RAM, 20GB storage
- **Recommended**: 4 CPU cores, 8GB RAM, 50GB SSD storage
- **OS**: Ubuntu 20.04+ or similar Linux distribution

### Production Checklist
- [ ] Set DEBUG=false in .env
- [ ] Use production Redis instance
- [ ] Set up proper logging
- [ ] Configure reverse proxy (Nginx)
- [ ] Set up SSL certificates
- [ ] Configure firewall
- [ ] Set up monitoring
- [ ] Configure backups
- [ ] Test disaster recovery

### Environment Variables for Production
```bash
# Production .env
DEBUG=false
GOOGLE_API_KEY=your_production_api_key
REDIS_URL=redis://your-redis-host:6379/0
CELERY_BROKER_URL=redis://your-redis-host:6379/1
CELERY_RESULT_BACKEND=redis://your-redis-host:6379/2
AI_MODEL=gemini-1.5-flash
CACHE_TTL=3600
MAX_REQUEST_SIZE=10000

# Additional production settings
SECRET_KEY=your-super-secret-key
ALLOWED_HOSTS=yourdomain.com,api.yourdomain.com
CORS_ORIGINS=https://yourfrontend.com
LOG_LEVEL=INFO
```

## 🔍 Troubleshooting

### Common Issues

#### 1. Redis Connection Error
```bash
# Error: Redis connection failed
# Solution: Check if Redis is running
redis-cli ping

# If not running, start Redis
redis-server
```

#### 2. Google API Key Error
```bash
# Error: Invalid API key
# Solution: Check your API key in .env file
# Make sure it's valid and has proper permissions
```

#### 3. Import Errors
```bash
# Error: Module not found
# Solution: Activate virtual environment
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt
```

#### 4. Port Already in Use
```bash
# Error: Port 8000 already in use
# Solution: Kill process using the port
lsof -ti:8000 | xargs kill -9

# Or use different port
uvicorn app.main:app --port 8001
```

#### 5. Celery Worker Not Starting
```bash
# Check Redis connection
redis-cli ping

# Check if broker URL is correct in .env
# Start worker with debug info
celery -A app.workers.celery_worker worker --loglevel=debug
```

### Debug Mode
```bash
# Enable debug logging
export DEBUG=true

# Or in .env file
DEBUG=true

# View detailed logs
tail -f logs/app.log
```

### Performance Issues
```bash
# Check system resources
htop

# Check Redis memory usage
redis-cli info memory

# Monitor API response times
curl -w "@curl-format.txt" -o /dev/null -s "http://localhost:8000/api/v1/health/"

# Create curl-format.txt:
echo "     time_namelookup:  %{time_namelookup}\n
        time_connect:  %{time_connect}\n
     time_appconnect:  %{time_appconnect}\n
    time_pretransfer:  %{time_pretransfer}\n
       time_redirect:  %{time_redirect}\n
  time_starttransfer:  %{time_starttransfer}\n
                     ----------\n
          time_total:  %{time_total}\n" > curl-format.txt
```

## 📚 API Usage Examples

### Python Client
```python
import requests

# Initialize client
base_url = "http://localhost:8000/api/v1"

# Synchronous summarization
response = requests.post(f"{base_url}/ai/summarize", json={
    "text": "Your long text here...",
    "max_length": 150
})
result = response.json()
print(result["data"]["summary"])

# Asynchronous processing
async_response = requests.post(f"{base_url}/ai/summarize/async", json={
    "text": "Your long text here...",
    "max_length": 150
})
job_id = async_response.json()["data"]["job_id"]

# Check job status
status_response = requests.get(f"{base_url}/jobs/{job_id}")
print(status_response.json())
```

### JavaScript/Node.js Client
```javascript
const axios = require('axios');

const baseURL = 'http://localhost:8000/api/v1';

// Summarize text
async function summarizeText(text, maxLength = 200) {
    try {
        const response = await axios.post(`${baseURL}/ai/summarize`, {
            text: text,
            max_length: maxLength
        });
        return response.data;
    } catch (error) {
        console.error('Error:', error.response.data);
    }
}

// Usage
summarizeText("Your text here...").then(result => {
    console.log(result.data.summary);
});
```

### cURL Examples
```bash
# Health check
curl http://localhost:8000/api/v1/health/

# Summarize text
curl -X POST "http://localhost:8000/api/v1/ai/summarize" \
  -H "Content-Type: application/json" \
  -d '{"text": "Your text here...", "max_length": 100}'

# Question answering
curl -X POST "http://localhost:8000/api/v1/ai/question-answer" \
  -H "Content-Type: application/json" \
  -d '{"context": "Context here...", "question": "Your question?"}'

# Tone rewriting
curl -X POST "http://localhost:8000/api/v1/ai/tone-rewrite" \
  -H "Content-Type: application/json" \
  -d '{"text": "Casual text here", "target_tone": "formal"}'

# Translation
curl -X POST "http://localhost:8000/api/v1/ai/translate" \
  -H "Content-Type: application/json" \
  -d '{"text": "Hello world", "target_language": "Spanish"}'
```

## 🎯 Next Steps

After successful implementation:

1. **Customize for Your Needs**
   - Add custom AI prompts
   - Implement additional endpoints
   - Add authentication/authorization
   - Integrate with your existing systems

2. **Scale the Service**
   - Set up load balancing
   - Implement horizontal scaling
   - Add database for persistent storage
   - Set up monitoring and alerting

3. **Enhance Security**
   - Implement API key authentication
   - Add rate limiting
   - Set up HTTPS
   - Regular security audits

4. **Monitor and Optimize**
   - Set up application monitoring
   - Optimize performance
   - Monitor costs (API usage)
   - Regular maintenance

## 📞 Support

If you encounter issues:
1. Check the troubleshooting section above
2. Review the logs in `logs/app.log`
3. Test with the demo client: `python examples/client_demo.py`
4. Check the API documentation at `http://localhost:8000/docs`
5. Create an issue in the repository with detailed error information

## 🎉 Congratulations!

You now have a fully functional AI Backend Service with:
- ✅ Text summarization
- ✅ Question answering
- ✅ Tone rewriting
- ✅ Translation
- ✅ Async processing
- ✅ Caching
- ✅ Monitoring
- ✅ Production-ready deployment options

The service is ready for development, testing, and production use!