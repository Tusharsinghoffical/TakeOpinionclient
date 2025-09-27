@echo off
echo TakeOpinion Deployment Script
echo ============================

echo Adding all changes to git...
git add .

echo Committing changes...
git commit -m "Fix module name truncation issue: Added explicit environment variable handling and debug scripts for Render deployment"

if %errorlevel% neq 0 (
    echo Error occurred during commit. Please check the status.
    pause
    exit /b %errorlevel%
)

echo Pushing to GitHub...
git push origin main

if %errorlevel% neq 0 (
    echo Error occurred during push. Please check your connection.
    pause
    exit /b %errorlevel%
)

echo Deployment completed successfully!
echo Please monitor your Render dashboard for deployment status.
pause