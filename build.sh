#!/usr/bin/env bash
# exit on error
set -o errexit

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "Installing dependencies from requirements.txt..."
pip install -r requirements.txt

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --no-input --verbosity=1

# Run migrations
echo "Running migrations..."
python manage.py migrate --verbosity=1

echo "Build completed successfully!"