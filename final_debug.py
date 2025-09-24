#!/usr/bin/env python
"""
Final comprehensive debug script for Render deployment issues
"""

import os
import sys
import importlib

def debug_environment():
    print("=== ENVIRONMENT DEBUG ===")
    print(f"Python version: {sys.version}")
    print(f"Current working directory: {os.getcwd()}")
    
    # Check Python path
    print("\nPython path:")
    for i, path in enumerate(sys.path):
        print(f"  {i:2d}: {path}")
    
    # Check environment variables
    print("\nKey environment variables:")
    important_vars = ['DJANGO_SETTINGS_MODULE', 'PYTHONPATH', 'PATH']
    for var in important_vars:
        value = os.environ.get(var, '<not set>')
        print(f"  {var}: {value}")
    
    # Check for any variables containing 'akeopinion'
    print("\nChecking for 'akeopinion' in environment:")
    found_akeopinion = False
    for key, value in os.environ.items():
        if 'akeopinion' in key.lower() or 'akeopinion' in value.lower():
            print(f"  {key}: {value}")
            found_akeopinion = True
    if not found_akeopinion:
        print("  No 'akeopinion' found in environment variables")

def debug_directory_structure():
    print("\n=== DIRECTORY STRUCTURE DEBUG ===")
    try:
        cwd = os.getcwd()
        print(f"Current directory: {cwd}")
        
        items = os.listdir(cwd)
        print(f"Items in current directory:")
        takeopinion_found = False
        for item in sorted(items):
            item_path = os.path.join(cwd, item)
            if os.path.isdir(item_path):
                print(f"  [DIR]  {item}")
                if item == 'takeopinion':
                    takeopinion_found = True
                    # List contents of takeopinion directory
                    try:
                        takeopinion_items = os.listdir(item_path)
                        print(f"    Contents of takeopinion:")
                        for subitem in sorted(takeopinion_items):
                            subitem_path = os.path.join(item_path, subitem)
                            if os.path.isdir(subitem_path):
                                print(f"      [DIR]  {subitem}")
                            else:
                                print(f"      [FILE] {subitem}")
                    except Exception as e:
                        print(f"    Error listing takeopinion contents: {e}")
            else:
                print(f"  [FILE] {item}")
        
        if not takeopinion_found:
            print("  ERROR: 'takeopinion' directory NOT found!")
            # List all directories to see what's there
            print("  All directories found:")
            for item in sorted(items):
                item_path = os.path.join(cwd, item)
                if os.path.isdir(item_path):
                    print(f"    [DIR]  {item}")
                    
    except Exception as e:
        print(f"Error checking directory structure: {e}")

def debug_imports():
    print("\n=== IMPORT DEBUG ===")
    
    # Test 1: Direct import
    print("Test 1: Direct import of takeopinion")
    try:
        import takeopinion
        print(f"  ✓ Success: takeopinion imported")
        print(f"    __file__: {getattr(takeopinion, '__file__', 'NO __file__')}")
        print(f"    __path__: {getattr(takeopinion, '__path__', 'NO __path__')}")
    except Exception as e:
        print(f"  ✗ Failed: {e}")
        import traceback
        traceback.print_exc()
    
    # Test 2: Import settings
    print("\nTest 2: Import takeopinion.settings")
    try:
        import takeopinion.settings
        print(f"  ✓ Success: takeopinion.settings imported")
    except Exception as e:
        print(f"  ✗ Failed: {e}")
        import traceback
        traceback.print_exc()
    
    # Test 3: Import settings_prod
    print("\nTest 3: Import takeopinion.settings_prod")
    try:
        import takeopinion.settings_prod
        print(f"  ✓ Success: takeopinion.settings_prod imported")
    except Exception as e:
        print(f"  ✗ Failed: {e}")
        import traceback
        traceback.print_exc()
    
    # Test 4: Manual import using importlib (like Django does)
    print("\nTest 4: Manual import using importlib")
    try:
        settings_module = os.environ.get('DJANGO_SETTINGS_MODULE', 'takeopinion.settings_prod')
        print(f"  Importing: {settings_module}")
        mod = importlib.import_module(settings_module)
        print(f"  ✓ Success: {settings_module} imported")
        print(f"    Module file: {mod.__file__}")
    except Exception as e:
        print(f"  ✗ Failed: {e}")
        import traceback
        traceback.print_exc()

def debug_django_setup():
    print("\n=== DJANGO SETUP DEBUG ===")
    try:
        import django
        from django.conf import settings
        
        print("  Django imported successfully")
        
        # Try to access a setting
        try:
            debug_value = settings.DEBUG
            print(f"  DEBUG setting: {debug_value}")
        except Exception as e:
            print(f"  Error accessing DEBUG setting: {e}")
            
        # Try to access INSTALLED_APPS
        try:
            app_count = len(settings.INSTALLED_APPS)
            print(f"  INSTALLED_APPS count: {app_count}")
        except Exception as e:
            print(f"  Error accessing INSTALLED_APPS: {e}")
            
        print("  Django setup test completed")
        
    except Exception as e:
        print(f"  Django setup failed: {e}")
        import traceback
        traceback.print_exc()

def main():
    print("Starting comprehensive debug...")
    debug_environment()
    debug_directory_structure()
    debug_imports()
    debug_django_setup()
    print("\n=== DEBUG COMPLETE ===")

if __name__ == "__main__":
    main()