@echo off
echo TakeOpinion Database Management
echo ==============================

REM Activate virtual environment
echo Activating virtual environment...
call .venv\Scripts\activate.bat

echo.
echo Select an option:
echo 1. Apply migrations
echo 2. Create migrations
echo 3. Reset database (WARNING: This will delete all data!)
echo 4. Create superuser
echo 5. Show migrations
echo.
choice /c 12345 /m "Enter your choice"

if %errorlevel% == 1 (
    echo Applying migrations...
    python manage.py migrate
) else if %errorlevel% == 2 (
    echo Creating migrations...
    python manage.py makemigrations
) else if %errorlevel% == 3 (
    echo WARNING: This will delete all data!
    choice /m "Are you sure you want to continue"
    if %errorlevel% == 1 (
        echo Deleting database...
        del db.sqlite3
        echo Applying migrations...
        python manage.py migrate
        echo Database reset completed.
    ) else (
        echo Operation cancelled.
    )
) else if %errorlevel% == 4 (
    echo Creating superuser...
    python manage.py createsuperuser
) else if %errorlevel% == 5 (
    echo Showing migrations...
    python manage.py showmigrations
)

pause