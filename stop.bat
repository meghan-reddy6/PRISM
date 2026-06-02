@echo off
setlocal

echo =========================================
echo Stopping Markdownify...
echo =========================================

:: Stop and remove containers
docker-compose down

:: Clean up temp uploads (Optional - preserving by default as requested, just cleaning empty dirs if needed)
echo [INFO] Containers stopped. Uploaded files preserved in /uploads and /outputs.

echo =========================================
echo Application stopped successfully.
echo =========================================
pause