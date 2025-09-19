@echo off
echo TakeOpinion Deployment Script
echo =============================

REM Check if virtual environment exists, if not create it
if not exist ".venv" (
    echo Creating virtual environment...
    python -m venv .venv
)

REM Activate virtual environment
echo Activating virtual environment...
call .venv\Scripts\activate.bat

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip

REM Install requirements
echo Installing requirements...
pip install -r requirements.txt

REM Collect static files
echo Collecting static files...
python manage.py collectstatic --noinput

REM Apply migrations
echo Applying database migrations...
python manage.py migrate

REM Create superuser if it doesn't exist (optional)
echo from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', 'admin@example.com', 'admin') if not User.objects.filter(username='admin').exists() else None | python manage.py shell

echo.
echo Deployment completed successfully!
echo.
echo To run the application in production mode, use:
echo python manage.py runserver --settings=takeopinion.settings_prod
echo.
echo For production deployment, consider using a proper web server like Nginx with Gunicorn or uWSGI.
pause