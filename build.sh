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
python -m pip install --upgrade pip

# Install dependencies
echo "=== Installing dependencies ==="
python -m pip install -r requirements.txt

# Collect static files
echo "=== Collecting static files ==="
python manage.py collectstatic --no-input --clear

# Run migrations
echo "=== Running migrations ==="
python manage.py migrate --no-input

# Import data if fixtures exist
echo "=== Importing data ==="
if [ -d "fixtures" ] && [ "$(ls -A fixtures)" ]; then
    echo "Fixtures directory found with data, importing..."
    python scripts/import_data.py
else
    echo "No fixtures directory found or empty, skipping data import"
fi

echo "=== Build completed successfully! ==="