#!/usr/bin/env bash
# exit on error
set -o errexit

# Enhanced build script for Render deployment
echo "=== Starting Enhanced Build Process ==="

# Debug: Print environment information
echo "Python version: $(python --version)"
echo "Current directory: $(pwd)"
echo "Contents of current directory:"
ls -la

# Explicitly set the Django settings module
export DJANGO_SETTINGS_MODULE=takeopinion.settings_prod

# Debug: Print the settings module being used
echo "Using DJANGO_SETTINGS_MODULE: $DJANGO_SETTINGS_MODULE"

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

# Debug: Check if gunicorn is installed
echo "=== Checking gunicorn installation ==="
if python -c "import gunicorn; print('Gunicorn version:', gunicorn.__version__)"; then
    echo "Gunicorn is properly installed"
else
    echo "ERROR: Gunicorn is not properly installed"
    pip list | grep gunicorn
    # Try to install gunicorn specifically
    pip install gunicorn
    if python -c "import gunicorn; print('Gunicorn version:', gunicorn.__version__)"; then
        echo "Gunicorn installed successfully"
    else
        echo "ERROR: Failed to install gunicorn"
        exit 1
    fi
fi

# Check if Pillow is properly installed
echo "=== Verifying Pillow installation ==="
python -c "from PIL import Image; print('Pillow is properly installed')"

# Collect static files with verbose output
echo "=== Collecting static files ==="
python manage.py collectstatic --no-input --verbosity=2 --clear

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