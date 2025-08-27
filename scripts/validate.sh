#!/bin/bash

# Validation script for AI Backend Service
echo "🔍 Validating AI Backend Service Setup..."
echo "=" * 50

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print status
print_status() {
    if [ $1 -eq 0 ]; then
        echo -e "${GREEN}✅ $2${NC}"
    else
        echo -e "${RED}❌ $2${NC}"
    fi
}

# Function to print warning
print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

# Check Python version
echo "Checking Python version..."
python3 --version > /dev/null 2>&1
print_status $? "Python 3 is installed"

# Check if virtual environment exists
echo "Checking virtual environment..."
if [ -d "venv" ]; then
    print_status 0 "Virtual environment exists"
else
    print_status 1 "Virtual environment not found"
    echo "Run: python3 -m venv venv"
fi

# Check if .env file exists
echo "Checking environment configuration..."
if [ -f ".env" ]; then
    print_status 0 ".env file exists"
    
    # Check if Google API key is set
    if grep -q "GOOGLE_API_KEY=your_google_api_key_here" .env; then
        print_warning "Google API key not configured in .env"
    elif grep -q "GOOGLE_API_KEY=" .env; then
        print_status 0 "Google API key is configured"
    else
        print_status 1 "Google API key not found in .env"
    fi
else
    print_status 1 ".env file not found"
    echo "Run: cp .env.example .env"
fi

# Check Redis connection
echo "Checking Redis connection..."
redis-cli ping > /dev/null 2>&1
print_status $? "Redis server is running"

# Check if dependencies are installed
echo "Checking Python dependencies..."
if [ -d "venv" ]; then
    source venv/bin/activate
    python -c "import fastapi, uvicorn, celery, redis, google.generativeai" > /dev/null 2>&1
    print_status $? "Required Python packages are installed"
else
    print_warning "Cannot check dependencies - virtual environment not found"
fi

# Check if logs directory exists
echo "Checking logs directory..."
if [ -d "logs" ]; then
    print_status 0 "Logs directory exists"
else
    mkdir -p logs
    print_status 0 "Created logs directory"
fi

# Check if scripts are executable
echo "Checking script permissions..."
if [ -x "scripts/start.sh" ]; then
    print_status 0 "Scripts are executable"
else
    chmod +x scripts/*.sh
    print_status 0 "Made scripts executable"
fi

# Test API server (if running)
echo "Testing API server..."
curl -s http://localhost:8000/api/v1/health/ > /dev/null 2>&1
if [ $? -eq 0 ]; then
    print_status 0 "API server is running and responding"
    
    # Test a simple endpoint
    response=$(curl -s http://localhost:8000/api/v1/health/ | grep -o '"status":"[^"]*"' | cut -d'"' -f4)
    if [ "$response" = "healthy" ]; then
        print_status 0 "API health check passed"
    else
        print_status 1 "API health check failed"
    fi
else
    print_warning "API server is not running"
    echo "Start with: ./scripts/start.sh"
fi

# Check Celery worker (if running)
echo "Checking Celery worker..."
celery -A app.workers.celery_worker inspect active > /dev/null 2>&1
if [ $? -eq 0 ]; then
    print_status 0 "Celery worker is running"
else
    print_warning "Celery worker is not running"
    echo "Start with: ./scripts/start-worker.sh"
fi

echo ""
echo "🎯 Validation Summary:"
echo "=" * 30

# Final recommendations
echo ""
echo "📋 Next Steps:"
if [ ! -f ".env" ]; then
    echo "1. Create .env file: cp .env.example .env"
fi

if grep -q "GOOGLE_API_KEY=your_google_api_key_here" .env 2>/dev/null; then
    echo "2. Add your Google API key to .env file"
fi

if ! redis-cli ping > /dev/null 2>&1; then
    echo "3. Start Redis server: redis-server"
fi

if ! curl -s http://localhost:8000/api/v1/health/ > /dev/null 2>&1; then
    echo "4. Start API server: ./scripts/start.sh"
fi

if ! celery -A app.workers.celery_worker inspect active > /dev/null 2>&1; then
    echo "5. Start Celery worker: ./scripts/start-worker.sh"
fi

echo ""
echo "🚀 Once everything is running, test with:"
echo "   python examples/client_demo.py"
echo "   or visit: http://localhost:8000/docs"

echo ""
echo "✨ Validation complete!"