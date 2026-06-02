@echo off
setlocal

echo =========================================
echo Starting Markdownify...
echo =========================================

:: Check if Docker is running
docker info >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Docker is not running. Please start Docker Desktop and try again.
    pause
    exit /b 1
)

:: Ensure .env exists
if not exist .env (
    echo [INFO] .env file not found. Creating from .env.example...
    copy .env.example .env
)

:: Start the containers
echo [INFO] Building and starting Docker containers...
docker-compose up -d --build

:: Wait a few seconds for the app to initialize
echo [INFO] Waiting for Streamlit to initialize...
timeout /t 5 /nobreak >nul

:: Open the browser
echo [INFO] Opening application in default browser...
start http://localhost:8501

echo =========================================
echo Application is running at http://localhost:8501
echo To stop the application, run stop.bat
echo =========================================
pause