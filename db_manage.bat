@echo off
title TakeOpinion Database Management
echo ========================================
echo TakeOpinion Database Management
echo ========================================
echo.

:menu
echo Select an option:
echo 1. Make migrations
echo 2. Apply migrations
echo 3. Create superuser
echo 4. Reset database (WARNING: This will delete all data!)
echo 5. Exit
echo.
set /p choice="Enter your choice (1-5): "

if "%choice%"=="1" goto makemigrations
if "%choice%"=="2" goto migrate
if "%choice%"=="3" goto createsuperuser
if "%choice%"=="4" goto resetdb
if "%choice%"=="5" goto exit
echo Invalid choice. Please try again.
echo.
goto menu

:makemigrations
echo.
echo Creating migrations...
python manage.py makemigrations
echo.
pause
goto menu

:migrate
echo.
echo Applying migrations...
python manage.py migrate
echo.
pause
goto menu

:createsuperuser
echo.
echo Creating superuser...
python manage.py createsuperuser
echo.
pause
goto menu

:resetdb
echo.
echo WARNING: This will delete all data!
set /p confirm="Are you sure you want to continue? (yes/no): "
if /i "%confirm%"=="yes" (
    echo Deleting database...
    del db.sqlite3
    echo Deleting migration files...
    for /d %%i in (accounts\migrations\*, blogs\migrations\*, bookings\migrations\*, core\migrations\*, doctors\migrations\*, feedbacks\migrations\*, hospitals\migrations\*, treatments\migrations\*) do (
        for %%j in (%%i\*.py) do (
            if not "%%~nj"=="__init__" (
                del "%%j"
            )
        )
    )
    echo Creating new migrations...
    python manage.py makemigrations
    echo Applying migrations...
    python manage.py migrate
    echo.
    echo Database reset complete!
) else (
    echo Database reset cancelled.
)
echo.
pause
goto menu

:exit
echo.
echo Goodbye!
exit /b