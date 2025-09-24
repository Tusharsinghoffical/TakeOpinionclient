#!/usr/bin/env python
"""
Deployment verification script for the TakeOpinion application.
This script checks if all required components are properly configured for deployment.
"""

import os
import sys
import importlib.util

def check_file_exists(filepath, description):
    """Check if a file exists and report the result."""
    if os.path.exists(filepath):
        print(f"✓ {description} found")
        return True
    else:
        print(f"✗ {description} not found")
        return False

def check_environment_variable(var_name, description):
    """Check if an environment variable is set."""
    if os.environ.get(var_name):
        print(f"✓ {description} is set")
        return True
    else:
        print(f"✗ {description} is not set")
        return False

def check_python_package(package_name, description):
    """Check if a Python package is installed."""
    try:
        importlib.util.find_spec(package_name)
        print(f"✓ {description} is installed")
        return True
    except ImportError:
        print(f"✗ {description} is not installed")
        return False

def main():
    print("TakeOpinion Deployment Verification")
    print("=" * 40)
    
    # Check required files
    print("\nChecking required files:")
    files_to_check = [
        ("takeopinion/settings.py", "Django settings file"),
        ("takeopinion/settings_prod.py", "Production settings file"),
        ("takeopinion/wsgi.py", "WSGI application file"),
        ("build.sh", "Build script"),
        ("requirements.txt", "Dependencies file"),
        ("render.yaml", "Render configuration file"),
    ]
    
    all_files_found = True
    for filepath, description in files_to_check:
        if not check_file_exists(filepath, description):
            all_files_found = False
    
    # Check required environment variables
    print("\nChecking environment variables:")
    env_vars_to_check = [
        ("DJANGO_SETTINGS_MODULE", "Django settings module"),
        ("SECRET_KEY", "Secret key"),
    ]
    
    all_env_vars_set = True
    for var_name, description in env_vars_to_check:
        if not check_environment_variable(var_name, description):
            all_env_vars_set = False
    
    # Check required Python packages
    print("\nChecking required Python packages:")
    packages_to_check = [
        ("django", "Django framework"),
        ("gunicorn", "Gunicorn WSGI server"),
        ("whitenoise", "WhiteNoise static files"),
        ("dj_database_url", "Database URL parser"),
    ]
    
    all_packages_installed = True
    for package_name, description in packages_to_check:
        if not check_python_package(package_name, description):
            all_packages_installed = False
    
    # Summary
    print("\n" + "=" * 40)
    if all_files_found and all_env_vars_set and all_packages_installed:
        print("✓ All checks passed! Ready for deployment.")
        return 0
    else:
        print("✗ Some checks failed. Please review the issues above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())