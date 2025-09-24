#!/usr/bin/env python
"""
Debug Django settings import issues
"""

import os
import sys

# Add current directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

print("Current directory:", current_dir)
print("Python path:")
for i, path in enumerate(sys.path):
    print(f"  {i}: {path}")

# Test different ways of importing
print("\n=== Testing Direct Imports ===")
try:
    import takeopinion
    print("✓ import takeopinion - SUCCESS")
    print(f"  Package file: {takeopinion.__file__}")
except Exception as e:
    print(f"✗ import takeopinion - FAILED: {e}")

try:
    from takeopinion import settings
    print("✓ from takeopinion import settings - SUCCESS")
except Exception as e:
    print(f"✗ from takeopinion import settings - FAILED: {e}")

try:
    import takeopinion.settings
    print("✓ import takeopinion.settings - SUCCESS")
except Exception as e:
    print(f"✗ import takeopinion.settings - FAILED: {e}")

try:
    import takeopinion.settings_prod
    print("✓ import takeopinion.settings_prod - SUCCESS")
except Exception as e:
    print(f"✗ import takeopinion.settings_prod - FAILED: {e}")

# Test Django setup
print("\n=== Testing Django Setup ===")
try:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'takeopinion.settings_prod')
    print(f"DJANGO_SETTINGS_MODULE set to: {os.environ.get('DJANGO_SETTINGS_MODULE')}")
    
    import django
    from django.conf import settings
    
    print("✓ Django imports successful")
    print(f"Settings module: {settings.__class__}")
    
    # Try to access a setting
    try:
        print(f"DEBUG setting: {settings.DEBUG}")
    except Exception as e:
        print(f"✗ Failed to access settings: {e}")
        
except Exception as e:
    print(f"✗ Django setup failed: {e}")
    import traceback
    traceback.print_exc()

# Check for any files with problematic names
print("\n=== Checking for Problematic Files ===")
def check_files(directory, pattern):
    import glob
    matches = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if pattern in file.lower():
                matches.append(os.path.join(root, file))
        for dir in dirs:
            if pattern in dir.lower():
                matches.append(os.path.join(root, dir))
    return matches

problematic_files = check_files('.', 'akeopinion')
if problematic_files:
    print("Found files/directories with 'akeopinion':")
    for f in problematic_files:
        print(f"  {f}")
else:
    print("No files/directories with 'akeopinion' found")

# Check the actual takeopinion directory
print("\n=== Checking takeopinion Directory ===")
if os.path.exists('takeopinion'):
    print("takeopinion directory exists")
    print("Contents:")
    try:
        contents = os.listdir('takeopinion')
        for item in contents:
            print(f"  {item}")
    except Exception as e:
        print(f"Error listing directory: {e}")
else:
    print("takeopinion directory does NOT exist")