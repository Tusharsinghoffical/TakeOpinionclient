#!/usr/bin/env python
"""
Test environment variables as they would be set by Render
"""

import os
import sys

# Simulate the exact environment variables that Render would set
test_env_vars = {
    "DJANGO_SETTINGS_MODULE": "takeopinion.settings_prod",
    "SECRET_KEY": "test-secret-key",
    "DEBUG": "False",
    "ALLOWED_HOSTS": ".onrender.com,takeopinionclient.onrender.com"
}

print("=== Setting Test Environment Variables ===")
for key, value in test_env_vars.items():
    os.environ[key] = value
    print(f"Set {key} = {value}")

print("\n=== Verifying Environment Variables ===")
for key, value in test_env_vars.items():
    actual_value = os.environ.get(key, "NOT SET")
    print(f"{key}: {actual_value}")
    if actual_value != value:
        print(f"  WARNING: Expected '{value}', got '{actual_value}'")

print("\n=== Testing Django Setup ===")
try:
    import django
    from django.conf import settings
    
    print("Django imported successfully")
    
    # This should trigger the settings loading
    print(f"DEBUG setting: {settings.DEBUG}")
    print(f"INSTALLED_APPS count: {len(settings.INSTALLED_APPS)}")
    
    print("Django setup completed successfully!")
    
except Exception as e:
    print(f"Django setup failed: {e}")
    import traceback
    traceback.print_exc()

print("\n=== Test Complete ===")