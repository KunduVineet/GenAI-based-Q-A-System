#!/bin/bash

# Setup script for the AI Backend Service
echo "Setting up AI Backend Service..."

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Copy environment file if it doesn't exist
if [ ! -f .env ]; then
    echo "Creating .env file from template..."
    cp .env.example .env
    echo "Please edit .env file and add your Google API key and other configurations."
fi

# Create logs directory
mkdir -p logs

# Make scripts executable
chmod +x scripts/*.sh

echo "Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env file and add your Google API key"
echo "2. Start Redis server: redis-server"
echo "3. Start the API server: ./scripts/start.sh"
echo "4. In another terminal, start the worker: ./scripts/start-worker.sh"