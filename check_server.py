#!/usr/bin/env python
"""
Health check script for the TakeOpinion application.
This script can be used to verify the application is running correctly.
"""

import os
import sys
import django
from django.conf import settings

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'takeopinion.settings_prod')

try:
    django.setup()
    print("Django setup successful")
    
    # Check if the database is accessible
    from django.db import connection
    with connection.cursor() as cursor:
        cursor.execute("SELECT 1")
        result = cursor.fetchone()
        if result:
            print("Database connection successful")
        else:
            print("Database connection failed")
    
    # Check if all apps are loaded
    from django.apps import apps
    loaded_apps = [app.name for app in apps.get_app_configs()]
    print(f"Loaded apps: {', '.join(loaded_apps)}")
    
    print("Health check completed successfully!")
    
except Exception as e:
    print(f"Health check failed: {e}")
    sys.exit(1)