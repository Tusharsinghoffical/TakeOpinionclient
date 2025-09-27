@echo off
echo === TakeOpinion Deployment Script ===
echo This script will prepare your application for deployment to Render
echo.

REM Check if Python is available
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.11 or later
    pause
    exit /b 1
)

REM Check if Git is available
git --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Git is not installed or not in PATH
    echo Please install Git
    pause
    exit /b 1
)

REM Export database data
echo Exporting database data...
python export_data.py
if %errorlevel% neq 0 (
    echo Error: Failed to export database data
    pause
    exit /b 1
)

REM Add all changes to git
echo Adding changes to git...
git add .

REM Commit changes
echo Committing changes...
git commit -m "Deployment update - %date% %time%"

REM Push to GitHub
echo Pushing to GitHub...
git push origin main
if %errorlevel% neq 0 (
    echo Error: Failed to push to GitHub
    echo Please check your Git configuration and try again
    pause
    exit /b 1
)

echo.
echo === Deployment preparation completed successfully! ===
echo.
echo Next steps:
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