@echo off
title TakeOpinion Development Server
echo ========================================
echo Starting TakeOpinion Development Server
echo ========================================
echo.
echo Server will be available at: http://127.0.0.1:8000/
echo Press CTRL+C to stop the server
echo.
pause
python manage.py runserver