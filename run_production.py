"""
Production WSGI server for TakeOpinion.

This script can be used to run the application with a production WSGI server.
"""

import os
import sys
from django.core.wsgi import get_wsgi_application

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'takeopinion.settings_prod')

# Get the WSGI application
application = get_wsgi_application()

if __name__ == "__main__":
    # This is just for testing purposes
    # In production, you would use a proper WSGI server like Gunicorn
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)