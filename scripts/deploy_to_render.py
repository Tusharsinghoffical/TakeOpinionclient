#!/usr/bin/env python
"""
Deployment script for TakeOpinion to Render
"""
import os
import subprocess
import sys
import json
from datetime import datetime

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

def check_git_status():
    """Check if git repository is clean"""
    print("Checking git status...")
    result = run_command("git status --porcelain")
    if result and result.strip():
        print("Git repository has uncommitted changes. Please commit or stash them before deployment.")
        return False
    return True

def export_database():
    """Export current database data"""
    print("Exporting database data...")
    result = run_command("python export_data.py")
    return result is not None

def commit_changes():
    """Commit all changes to git"""
    print("Committing changes...")
    commands = [
        "git add .",
        'git commit -m "Deployment update - {}"'.format(datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
        "git push origin main"
    ]
    
    for command in commands:
        result = run_command(command)
        if result is None:
            return False
    return True

def main():
    """Main deployment function"""
    print("=== TakeOpinion Deployment to Render ===")
    print("This script will prepare your application for deployment to Render")
    
    # Check git status
    if not check_git_status():
        return False
    
    # Export database
    if not export_database():
        print("Failed to export database")
        return False
    
    # Commit changes
    if not commit_changes():
        print("Failed to commit changes")
        return False
    
    print("=== Deployment preparation completed successfully! ===")
    print("Next steps:")
    print("1. Go to your Render dashboard")
    print("2. Connect your GitHub repository")
    print("3. Configure the service with:")
    print("   - Build command: ./build.sh")
    print("   - Start command: gunicorn --bind 0.0.0.0:$PORT takeopinion.wsgi:application")
    print("   - Environment variables:")
    print("     - DJANGO_SETTINGS_MODULE=takeopinion.settings_prod")
    print("     - SECRET_KEY=(auto-generated or your own)")
    print("     - DEBUG=False")
    print("     - ALLOWED_HOSTS=.onrender.com,your-app-name.onrender.com")
    print("")
    print("Your data will be automatically imported during the build process!")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)