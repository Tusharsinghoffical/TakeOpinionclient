@echo off
echo Fixing patient dashboard 500 error...
echo.

echo Adding changes to git...
git add .

echo Committing changes...
git commit -m "Fix patient dashboard 500 error - Handle cases where users don't have profiles or patient details"

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