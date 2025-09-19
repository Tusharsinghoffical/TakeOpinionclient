#!/bin/bash
# Build script for Render deployment

# Exit on any error
set -e

# Install Python dependencies
echo "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput --verbosity=2

# Apply database migrations
echo "Applying database migrations..."
python manage.py migrate

echo "Build completed successfully!"