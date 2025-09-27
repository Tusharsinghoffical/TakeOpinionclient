#!/usr/bin/env bash
# exit on error
set -o errexit

# Simple build script for Render deployment
echo "=== Starting Build Process ==="

# Explicitly set the Django settings module to avoid truncation issues
export DJANGO_SETTINGS_MODULE=takeopinion.settings_prod

# Debug: Print the settings module being used
echo "Using DJANGO_SETTINGS_MODULE: $DJANGO_SETTINGS_MODULE"

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

# Import data if fixtures exist
echo "=== Importing data ==="
if [ -d "fixtures" ]; then
    echo "Fixtures directory found, importing data..."
    python scripts/import_data.py
else
    echo "No fixtures directory found, skipping data import"
fi

echo "=== Build completed successfully! ==="