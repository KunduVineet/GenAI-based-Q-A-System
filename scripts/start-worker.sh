#!/bin/bash

# Start script for Celery worker
echo "Starting Celery worker..."

# Check if .env file exists
if [ ! -f .env ]; then
    echo "Error: .env file not found. Please copy .env.example to .env and configure it."
    exit 1
fi

# Check if Redis is running
redis-cli ping > /dev/null 2>&1
if [ $? -ne 0 ]; then
    echo "Warning: Redis server is not running. Please start Redis first."
    echo "You can start Redis with: redis-server"
    exit 1
fi

# Create logs directory
mkdir -p logs

# Start Celery worker
echo "Starting Celery worker..."
celery -A app.workers.celery_worker worker --loglevel=info --concurrency=2