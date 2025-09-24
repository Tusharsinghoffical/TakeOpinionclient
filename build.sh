#!/usr/bin/env bash
# exit on error
set -o errexit

# Simple build script for Render deployment
echo "=== Starting Build Process ==="

# Upgrade pip
echo "=== Upgrading pip ==="
pip install --upgrade pip

# Install dependencies
echo "=== Installing dependencies ==="
pip install -r requirements.txt

# Collect static files
echo "=== Collecting static files ==="
python manage.py collectstatic --no-input

# Run migrations
echo "=== Running migrations ==="
python manage.py migrate

echo "=== Build completed successfully! ==="