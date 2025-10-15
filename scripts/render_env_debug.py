#!/usr/bin/env python
"""
Debug script to check environment variables on Render
"""
import os

def debug_env():
    """Print important environment variables for debugging"""
    print("=== Render Environment Debug ===")
    
    # Check key environment variables
    env_vars = [
        'DJANGO_SETTINGS_MODULE',
        'SECRET_KEY', 
        'DEBUG',
        'ALLOWED_HOSTS',
        'DATABASE_URL',
        'PORT',
        'PYTHON_VERSION',
        'RENDER'
    ]
    
    for var in env_vars:
        value = os.environ.get(var, '(not set)')
        # Mask sensitive values
        if var == 'SECRET_KEY' and value != '(not set)':
            value = f"{value[:5]}...{value[-5:]}" if len(value) > 10 else "****"
        print(f"{var}: {value}")
    
    print("=== End Environment Debug ===")

if __name__ == '__main__':
    debug_env()