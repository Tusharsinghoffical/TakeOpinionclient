#!/usr/bin/env python
"""
Simulate the exact Render environment and Django setup process
"""

import os
import sys

def simulate_render_environment():
    print("=== SIMULATING RENDER ENVIRONMENT ===")
    
    # Set the exact same environment variables as in render.yaml
    os.environ['DJANGO_SETTINGS_MODULE'] = 'takeopinion.settings_prod'
    os.environ['SECRET_KEY'] = 'test-key-for-simulation'
    os.environ['DEBUG'] = 'False'
    os.environ['ALLOWED_HOSTS'] = '.onrender.com,takeopinionclient.onrender.com'
    
    print("Environment variables set:")
    print(f"  DJANGO_SETTINGS_MODULE: {os.environ['DJANGO_SETTINGS_MODULE']}")
    print(f"  SECRET_KEY: {os.environ['SECRET_KEY']}")
    print(f"  DEBUG: {os.environ['DEBUG']}")
    print(f"  ALLOWED_HOSTS: {os.environ['ALLOWED_HOSTS']}")
    
    # Add current directory to Python path (this is what Python does)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    if current_dir not in sys.path:
        sys.path.insert(0, current_dir)
        print(f"Added to Python path: {current_dir}")
    
    print(f"Current working directory: {os.getcwd()}")
    print(f"Python path:")
    for i, path in enumerate(sys.path):
        print(f"  {i:2d}: {path}")

def test_django_import_process():
    print("\n=== TESTING DJANGO IMPORT PROCESS ===")
    
    # This is the exact process that Django's manage.py uses
    try:
        # Step 1: Get the settings module from environment
        settings_module = os.environ.get('DJANGO_SETTINGS_MODULE')
        print(f"1. Settings module from environment: {settings_module}")
        
        if not settings_module:
            print("   ERROR: DJANGO_SETTINGS_MODULE not set!")
            return False
            
        # Step 2: Import the settings module (this is where the error occurs in Render)
        print("2. Attempting to import settings module...")
        import importlib
        try:
            mod = importlib.import_module(settings_module)
            print(f"   ✓ Success: Imported {settings_module}")
            print(f"   Module file: {mod.__file__}")
        except ImportError as e:
            print(f"   ✗ ImportError: {e}")
            # Let's try to get more details about what's happening
            module_parts = settings_module.split('.')
            print(f"   Module parts: {module_parts}")
            
            # Try importing each part
            for i in range(len(module_parts)):
                partial_module = '.'.join(module_parts[:i+1])
                try:
                    partial_mod = importlib.import_module(partial_module)
                    print(f"   ✓ Partial import {partial_module}: SUCCESS")
                except ImportError as partial_e:
                    print(f"   ✗ Partial import {partial_module}: FAILED - {partial_e}")
                    # Check if the directory exists
                    if i == 0:  # This is the first part (takeopinion)
                        if os.path.exists(partial_module):
                            print(f"   Directory {partial_module} EXISTS")
                        else:
                            print(f"   Directory {partial_module} DOES NOT EXIST")
            return False
        except Exception as e:
            print(f"   ✗ Unexpected error: {e}")
            import traceback
            traceback.print_exc()
            return False
            
        # Step 3: Setup Django
        print("3. Setting up Django...")
        import django
        from django.conf import settings
        
        try:
            # This should work if the settings module was imported correctly
            debug_value = settings.DEBUG
            print(f"   ✓ Django setup successful, DEBUG = {debug_value}")
        except Exception as e:
            print(f"   ✗ Django setup failed: {e}")
            import traceback
            traceback.print_exc()
            return False
            
        return True
        
    except Exception as e:
        print(f"Unexpected error in Django import process: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    print("Starting Render environment simulation...")
    simulate_render_environment()
    success = test_django_import_process()
    
    if success:
        print("\n=== SIMULATION SUCCESSFUL ===")
        print("The Django setup process works correctly in this environment.")
    else:
        print("\n=== SIMULATION FAILED ===")
        print("There was an issue with the Django setup process.")
        
    print("\n=== SIMULATION COMPLETE ===")

if __name__ == "__main__":
    main()