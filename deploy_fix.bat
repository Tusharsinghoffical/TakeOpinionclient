@echo off
title TakeOpinion - Deploy Fix for 500 Error
echo ========================================
echo TakeOpinion - Deploy Fix for 500 Error
echo ========================================
echo.
echo This script will deploy the fix for the patient dashboard 500 error.
echo.

REM Add all changes to git
echo Adding all changes to git...
git add .

REM Commit changes
echo Committing changes...
git commit -m "Fix patient dashboard 500 error - undefined variables in template and view and add .gitignore"

REM Push to GitHub
echo Pushing to GitHub...
git push

echo.
echo Deployment completed successfully!
echo.
echo Next steps:
echo 1. Go to your Render dashboard
echo 2. Navigate to your web service
echo 3. Trigger a new deployment
echo 4. If you encounter issues, use "Clear build cache & deploy"
echo.
pause