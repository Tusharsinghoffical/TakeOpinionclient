#!/usr/bin/env bash
# exit on error
set -o errexit

# Debug information
echo "=== Build Debug Information ==="
echo "Current directory: $(pwd)"
echo "Python version: $(python --version)"
echo "Directory listing:"
ls -la

# Check if takeopinion directory exists
echo "=== Checking takeopinion directory ==="
if [ -d "takeopinion" ]; then
    echo "takeopinion directory exists"
    echo "Contents:"
    ls -la takeopinion
else
    echo "ERROR: takeopinion directory does NOT exist"
    exit 1
fi

# Check Python path and imports
echo "=== Testing Python imports ==="
python -c "
import sys
print('Python path:')
for p in sys.path:
    print('  ' + p)
    
print('Testing takeopinion import...')
try:
    import takeopinion
    print('✓ takeopinion imported successfully')
    print('  File:', takeopinion.__file__)
except Exception as e:
    print('✗ takeopinion import failed:', e)

print('Testing takeopinion.settings import...')
try:
    import takeopinion.settings
    print('✓ takeopinion.settings imported successfully')
except Exception as e:
    print('✗ takeopinion.settings import failed:', e)

print('Testing takeopinion.settings_prod import...')
try:
    import takeopinion.settings_prod
    print('✓ takeopinion.settings_prod imported successfully')
except Exception as e:
    print('✗ takeopinion.settings_prod import failed:', e)
"

# Upgrade pip
echo "=== Upgrading pip ==="
pip install --upgrade pip

# Install dependencies
echo "=== Installing dependencies ==="
pip install -r requirements.txt

# Collect static files
echo "=== Collecting static files ==="
python manage.py collectstatic --no-input --verbosity=2

# Run migrations
echo "=== Running migrations ==="
python manage.py migrate --verbosity=2

echo "=== Build completed successfully! ==="