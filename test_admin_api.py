import os
import sys
import django
from django.test import Client
from django.contrib.auth.models import User

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'takeopinion.settings')
django.setup()

# Create a test client
c = Client()

# Try to access the admin API
response = c.post('/accounts/admin/api/doctors/add/', {
    'name': 'Test Doctor',
    'specialization': 'Test Specialization',
    'email': 'test@example.com',
    'experience_years': 10
})

print(f"Status code: {response.status_code}")
print(f"Response: {response.json()}")