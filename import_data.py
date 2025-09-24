#!/usr/bin/env python
"""
Script to import database data after deployment
"""
import os
import django
from django.core.management import execute_from_command_line

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'takeopinion.settings')
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
        'accounts_data.json',
        'blogs_data.json',
        'bookings_data.json',
        'feedbacks_data.json'
    ]
    
    try:
        for fixture in fixture_files:
            fixture_path = f'fixtures/{fixture}'
            if os.path.exists(fixture_path):
                print(f"Importing {fixture}...")
                management.call_command('loaddata', fixture_path)
            else:
                print(f"Fixture {fixture} not found, skipping...")
        
        print("Data import completed successfully!")
        
    except Exception as e:
        print(f"Error importing data: {e}")

if __name__ == '__main__':
    import_data()