@echo off
echo Deploying TakeOpinion application to Render...

REM Add all changes
git add .

REM Commit changes
git commit -m "Fix patient dashboard 500 error - undefined variables"

REM Push to GitHub (assuming 'origin' is the remote name)
git push origin main

echo.
echo Deployment completed!
echo Please go to your Render dashboard and trigger a new deployment.
echo If you encounter issues, clear the build cache in Render settings.
pause
