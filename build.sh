#!/usr/bin/env bash
# exit on error
set -o errexit

# Simple build script for Render deployment
echo "=== Starting Build Process ==="

# Explicitly set the Django settings module to avoid truncation issues
export DJANGO_SETTINGS_MODULE=takeopinion.settings_prod

# Debug: Print the settings module being used
echo "Using DJANGO_SETTINGS_MODULE: $DJANGO_SETTINGS_MODULE"

# Run our debug script to check environment
echo "=== Running Environment Debug ==="
python render_env_debug.py

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