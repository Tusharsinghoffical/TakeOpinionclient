#!/usr/bin/env python
"""
Universal startup script that works on both Windows (local) and Linux (Render)
"""

import os
import sys
import platform

def start_server():
    """Start the appropriate server based on the environment"""
    
    # Check if we're running on Render (Linux environment)
    if platform.system() == 'Linux' or os.environ.get('RENDER'):
        print("Starting Gunicorn server for Render deployment...")
        # Import and start gunicorn
        try:
            from gunicorn.app.wsgiapp import WSGIApplication
            # This will be called by the render.yaml startCommand
            # We just print a message here for debugging
            print("Gunicorn server ready")
        except ImportError as e:
            print(f"Failed to import gunicorn: {e}")
            sys.exit(1)
    else:
        print("Starting Django development server for local development...")
        # Use Django's built-in development server for local Windows development
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'takeopinion.settings')
        try:
            from django.core.management import execute_from_command_line
            execute_from_command_line(['manage.py', 'runserver', '8000'])
        except Exception as e:
            print(f"Failed to start development server: {e}")
            sys.exit(1)

if __name__ == '__main__':
    start_server()