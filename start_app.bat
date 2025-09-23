@echo off
title TakeOpinion Development Server
echo ========================================
echo Starting TakeOpinion Development Server
echo ========================================
echo.
echo Installing requirements...
pip install -r requirements.txt
echo.
echo Making migrations...
python manage.py makemigrations
echo.
echo Applying migrations...
python manage.py migrate
echo.
echo Collecting static files...
python manage.py collectstatic --noinput
echo.
echo Starting server...
echo Server will be available at: http://127.0.0.1:8000/
echo Press CTRL+C to stop the server
echo.
pause
python manage.py runserver