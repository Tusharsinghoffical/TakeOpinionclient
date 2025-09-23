import os
import django

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'takeopinion.settings')
django.setup()

from django.conf import settings

print("Testing MongoDB connection...")

# Print database configuration
print(f"Database engine: {settings.DATABASES['default']['ENGINE']}")
print(f"Database name: {settings.DATABASES['default']['NAME']}")

# Get the connection string from settings
if 'CLIENT' in settings.DATABASES['default']:
    connection_string = settings.DATABASES['default']['CLIENT']['host']
else:
    connection_string = str(settings.DATABASES['default'].get('host', ''))

print(f"Connection string: {connection_string}")

print("\nTest completed!")