@echo off
title TakeOpinion - Medical Tourism Platform
echo ==================================
echo TakeOpinion - Medical Tourism Platform
echo ==================================
echo.

REM Check if virtual environment exists
if not exist ".venv" (
    echo Creating virtual environment...
    python -m venv .venv
    echo.
)

REM Activate virtual environment
echo Activating virtual environment...
call .venv\Scripts\activate.bat
echo.

REM Check if requirements are installed
echo Checking requirements...
pip show django >nul 2>&1
if %errorlevel% neq 0 (
    echo Installing requirements...
    pip install -r requirements.txt
    echo.
)

REM Collect static files
echo Collecting static files...
python manage.py collectstatic --noinput
echo.

REM Apply migrations
echo Applying database migrations...
python manage.py migrate
echo.

echo ==================================
echo Setup completed successfully!
echo ==================================
echo.
echo Starting development server...
echo.
echo The application will be available at http://127.0.0.1:8000
echo.
echo To access the admin panel:
echo Username: admin
echo Password: admin
echo.
echo Press CTRL+C to stop the server
echo.
timeout /t 5 /nobreak >nul
python manage.py runserver