@echo off
title Deploy TakeOpinion with MongoDB
echo ========================================
echo Deploying TakeOpinion with MongoDB Support
echo ========================================
echo.

echo Adding changes to git...
git add .

echo Committing changes...
git commit -m "Configure MongoDB as database and update requirements"

echo Pushing to GitHub...
git push origin main

echo.
echo Changes have been pushed to GitHub!
echo.
echo Next steps:
echo 1. Go to your Render dashboard
echo 2. Navigate to your web service
echo 3. Trigger a new deployment
echo 4. If you encounter issues, use "Clear build cache & deploy"
echo.
pause