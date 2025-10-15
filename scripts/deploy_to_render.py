#!/usr/bin/env python
"""
Deployment script for TakeOpinion to Render
"""
import os
import subprocess
import sys
import json
from django.utils import timezone

def run_command(command, cwd=None):
    """Run a shell command and return the result"""
    try:
        print(f"Running: {command}")
        result = subprocess.run(
            command, 
            shell=True, 
            cwd=cwd, 
            capture_output=True, 
            text=True,
            check=True
        )
        print(result.stdout)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {command}")
        print(f"Error: {e.stderr}")
        return None

def export_database():
    """Export current database data"""
    print("Exporting database data...")
    result = run_command("python export_data.py")
    return result is not None

def main():
    """Main deployment function"""
    print("=== TakeOpinion Deployment Preparation ===")
    print("This script will prepare your application for deployment")
    
    # Export database
    if not export_database():
        print("Failed to export database")
        return False
    
    print("=== Deployment preparation completed successfully! ===")
    print("Next steps:")
    print("1. Configure your deployment environment")
    print("2. Set the required environment variables:")
    print("   - DJANGO_SETTINGS_MODULE=takeopinion.settings_prod")
    print("   - SECRET_KEY=(auto-generated or your own)")
    print("   - DEBUG=False")
    print("   - ALLOWED_HOSTS=.onrender.com,your-app-name.onrender.com")
    print("")
    print("Your data will be automatically imported during the build process!")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)