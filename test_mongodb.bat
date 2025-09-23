@echo off
title Test MongoDB Connection
echo ========================================
echo Testing MongoDB Connection
echo ========================================
echo.

echo Installing requirements...
pip install -r requirements.txt

echo.
echo Running MongoDB connection test...
python test_mongodb.py

echo.
pause