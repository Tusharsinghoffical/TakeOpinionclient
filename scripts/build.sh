#!/usr/bin/env bash
# exit on error
set -o errexit

# Enhanced build script for Render deployment
echo "=== Starting Enhanced Build Process ==="

# Explicitly set the Django settings module
export DJANGO_SETTINGS_MODULE=takeopinion.settings_prod

# Debug: Print the settings module being used
echo "Using DJANGO_SETTINGS_MODULE: $DJANGO_SETTINGS_MODULE"

# Run our debug script to check environment
echo "=== Running Environment Debug ==="
python scripts/render_env_debug.py

# Upgrade pip to latest version
echo "=== Upgrading pip ==="
pip install --upgrade pip

# Install dependencies with error handling
echo "=== Installing dependencies ==="
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
else
    echo "ERROR: requirements.txt not found!"
    exit 1
fi

# Check if Pillow is properly installed
echo "=== Verifying Pillow installation ==="
python -c "from PIL import Image; print('Pillow is properly installed')"

# Collect static files with verbose output
echo "=== Collecting static files ==="
python manage.py collectstatic --no-input --verbosity=2

# Run migrations
echo "=== Running migrations ==="
python manage.py migrate --no-input

# Create superuser if it doesn't exist (optional)
echo "=== Creating superuser (if needed) ==="
python manage.py shell -c "
from django.contrib.auth import get_user_model;
User = get_user_model();
if not User.objects.filter(is_superuser=True).exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123');
    print('Superuser created');
else:
    print('Superuser already exists');
"

# Import data if fixtures exist
echo "=== Importing data ==="
if [ -d "fixtures" ] && [ "$(ls -A fixtures)" ]; then
    echo "Fixtures directory found with data, importing..."
    python scripts/import_data.py
else
    echo "No fixtures directory found or empty, skipping data import"
fi

echo "=== Build completed successfully! ==="