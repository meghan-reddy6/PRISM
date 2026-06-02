#!/bin/bash

echo "========================================="
echo "Starting Markdownify..."
echo "========================================="

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
  echo "[ERROR] Docker is not running. Please start Docker and try again."
  exit 1
fi

# Ensure .env exists
if [ ! -f .env ]; then
  echo "[INFO] .env file not found. Creating from .env.example..."
  cp .env.example .env
fi

# Start the containers
echo "[INFO] Building and starting Docker containers..."
docker-compose up -d --build

# Wait a few seconds for the app to initialize
echo "[INFO] Waiting for Streamlit to initialize..."
sleep 5

# Open the browser automatically based on OS
echo "[INFO] Opening application in default browser..."
if which xdg-open > /dev/null
then
  xdg-open http://localhost:8501
elif which open > /dev/null
then
  open http://localhost:8501
else
  echo "Could not detect web browser. Please navigate to http://localhost:8501 manually."
fi

echo "========================================="
echo "Application is running at http://localhost:8501"
echo "To stop the application, run ./stop.sh"
echo "========================================="