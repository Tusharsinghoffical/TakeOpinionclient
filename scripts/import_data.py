#!/usr/bin/env python
"""
Script to import database data after deployment
"""
import os
import sys
import django
from django.core.management import execute_from_command_line

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'takeopinion.settings_prod')
django.setup()

from django.core import management

def import_data():
    """Import data using Django's loaddata command"""
    print("Importing data...")
    
    # Import data in the correct order to handle dependencies
    fixture_files = [
        'core_data.json',
        'treatments_data.json', 
        'hospitals_data.json',
        'doctors_data.json',
        'blogs_data.json',
        'comprehensive_medical_data.json',  # Use comprehensive data instead of separate accounts_data
        'bookings_data.json',
        'feedbacks_data.json'
    ]
    
    try:
        for fixture in fixture_files:
            fixture_path = f'fixtures/{fixture}'
            if os.path.exists(fixture_path):
                print(f"Importing {fixture}...")
                try:
                    management.call_command('loaddata', fixture_path)
                except Exception as e:
                    print(f"Warning: Could not import {fixture}: {e}")
            else:
                print(f"Fixture {fixture} not found, skipping...")
        
        print("Data import completed successfully!")
        
    except Exception as e:
        print(f"Error importing data: {e}")

if __name__ == '__main__':
    import_data()