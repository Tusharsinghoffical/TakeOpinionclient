#!/usr/bin/env python
"""
Script to export database data for deployment
"""
import os
import django
from django.core.management import execute_from_command_line

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'takeopinion.settings')
django.setup()

from django.core import management

def export_data():
    """Export data using Django's dumpdata command"""
    print("Exporting data...")
    
    # Export all data except contenttypes and auth permissions
    apps_to_export = [
        'core', 'treatments', 'hospitals', 'doctors', 
        'blogs', 'bookings', 'accounts', 'feedbacks', 'payments'
    ]
    
    try:
        # Create fixtures directory if it doesn't exist
        if not os.path.exists('fixtures'):
            os.makedirs('fixtures')
            
        for app in apps_to_export:
            print(f"Exporting {app}...")
            with open(f'fixtures/{app}_data.json', 'w') as f:
                management.call_command(
                    'dumpdata', 
                    app, 
                    indent=2, 
                    exclude=['contenttypes', 'auth.permission'],
                    stdout=f
                )
        
        print("Data export completed successfully!")
        
    except Exception as e:
        print(f"Error exporting data: {e}")

if __name__ == '__main__':
    export_data()