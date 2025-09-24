#!/usr/bin/env python
"""
Test Django setup exactly as it would happen in Render
"""

import os
import sys

# Add current directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

print("=== Testing Django Setup (Render Simulation) ===")
print(f"Current directory: {current_dir}")
print(f"Working directory: {os.getcwd()}")

# Set the exact same environment variables as in render.yaml
os.environ['DJANGO_SETTINGS_MODULE'] = 'takeopinion.settings_prod'
print(f"DJANGO_SETTINGS_MODULE set to: {os.environ.get('DJANGO_SETTINGS_MODULE')}")

# Test the import that's failing in Render
print("\n=== Testing Settings Import ===")
settings_module = os.environ.get('DJANGO_SETTINGS_MODULE')
if settings_module:
    try:
        import importlib
        print(f"Importing settings module: {settings_module}")
        
        # This is what Django does internally
        mod = importlib.import_module(settings_module)
        print(f"✓ Successfully imported {settings_module}")
        print(f"Module file: {mod.__file__}")
        
        # Check if it has the expected attributes
        if hasattr(mod, 'INSTALLED_APPS'):
            print(f"✓ INSTALLED_APPS found: {len(mod.INSTALLED_APPS)} apps")
        else:
            print("✗ INSTALLED_APPS not found")
            
        if hasattr(mod, 'DATABASES'):
            print(f"✓ DATABASES found: {list(mod.DATABASES.keys())}")
        else:
            print("✗ DATABASES not found")
            
    except Exception as e:
        print(f"✗ Failed to import {settings_module}: {e}")
        import traceback
        traceback.print_exc()
else:
    print("✗ DJANGO_SETTINGS_MODULE not set")

# Test Django setup
print("\n=== Testing Full Django Setup ===")
try:
    import django
    django.setup()  # This is the key step that was missing
    
    from django.conf import settings
    
    # This should trigger the settings loading
    debug_value = settings.DEBUG
    print(f"✓ Django setup successful, DEBUG = {debug_value}")
    
except Exception as e:
    print(f"✗ Django setup failed: {e}")
    import traceback
    traceback.print_exc()

# Test management command discovery
print("\n=== Testing Management Commands ===")
try:
    import django as django2
    django2.setup()  # Make sure Django is set up
    from django.core.management import get_commands
    commands = get_commands()
    if 'collectstatic' in commands:
        print("✓ 'collectstatic' command found")
    else:
        print("✗ 'collectstatic' command NOT found")
        print("Available commands:", list(commands.keys())[:10], "...")
except Exception as e:
    print(f"✗ Failed to get commands: {e}")
    import traceback
    traceback.print_exc()