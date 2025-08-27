#!/bin/bash

# Test script for the AI Backend Service
echo "Running tests for AI Backend Service..."

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Run tests with coverage
echo "Running pytest with coverage..."
pytest --cov=app --cov-report=html --cov-report=term-missing

echo "Test results:"
echo "- Coverage report generated in htmlcov/"
echo "- Open htmlcov/index.html in your browser to view detailed coverage"