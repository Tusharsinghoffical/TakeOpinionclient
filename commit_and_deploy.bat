@echo off
echo === TakeOpinion Commit and Deployment Script ===
echo This script will commit all changes and prepare for deployment
echo.

REM Check if Git is available
git --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Git is not installed or not in PATH
    echo Please install Git
    pause
    exit /b 1
)

echo Adding all changes to git...
git add .

echo Committing changes...
git commit -m "Deployment update - %date% %time%"

if %errorlevel% neq 0 (
    echo No changes to commit or error occurred
)

echo Pushing to GitHub...
git push origin main

if %errorlevel% neq 0 (
    echo Error: Failed to push to GitHub
    echo Please check your Git configuration and try again
    pause
    exit /b 1
)

echo.
echo === Changes committed and pushed successfully! ===
echo.
echo Now you can deploy to Render:
echo 1. Go to your Render dashboard
echo 2. Connect your GitHub repository
echo 3. Configure the service with:
echo    - Build command: ./build.sh
echo    - Start command: gunicorn --bind 0.0.0.0:$PORT takeopinion.wsgi:application
echo    - Environment variables:
echo      - DJANGO_SETTINGS_MODULE=takeopinion.settings_prod
echo      - SECRET_KEY=(auto-generated or your own)
echo      - DEBUG=False
echo      - ALLOWED_HOSTS=.onrender.com,your-app-name.onrender.com
echo.
echo Your data will be automatically imported during the build process!
echo.
pause