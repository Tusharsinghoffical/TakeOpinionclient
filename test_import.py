#!/usr/bin/env python
"""
Test script to verify Django settings import
"""

import os
import sys

# Add the project directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("Python path:")
for path in sys.path:
    print(f"  {path}")

print("\nTesting import of takeopinion.settings...")
try:
    import takeopinion.settings
    print("✓ takeopinion.settings imported successfully")
except Exception as e:
    print(f"✗ Failed to import takeopinion.settings: {e}")

print("\nTesting import of takeopinion.settings_prod...")
try:
    import takeopinion.settings_prod
    print("✓ takeopinion.settings_prod imported successfully")
except Exception as e:
    print(f"✗ Failed to import takeopinion.settings_prod: {e}")

print("\nTesting Django setup...")
try:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'takeopinion.settings_prod')
    import django
    django.setup()
    print("✓ Django setup successful")
except Exception as e:
    print(f"✗ Django setup failed: {e}")