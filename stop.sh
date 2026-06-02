#!/bin/bash

echo "========================================="
echo "Stopping Markdownify..."
echo "========================================="

# Stop and remove containers
docker-compose down

echo "[INFO] Containers stopped. User data preserved in ./uploads and ./outputs."
echo "========================================="
echo "Application stopped successfully."
echo "========================================="