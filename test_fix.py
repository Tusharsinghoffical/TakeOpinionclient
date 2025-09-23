import os
import django

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'takeopinion.settings')
django.setup()

from django.contrib.auth.models import User
from accounts.models import UserProfile, PatientProfile
from accounts.views import patient_dashboard
from django.http import HttpRequest
from django.contrib.auth.models import AnonymousUser
from django.contrib.messages.middleware import MessageMiddleware
from django.contrib.sessions.middleware import SessionMiddleware

# Create a mock request object
def create_mock_request(user):
    request = HttpRequest()
    request.user = user
    
    # Add session and message middleware
    SessionMiddleware().process_request(request)
    MessageMiddleware().process_request(request)
    
    request.session.save()
    return request

# Test with a user that has no profile
print("Testing with user that has no profile...")
try:
    user = User.objects.get(username='admin')  # This user has no profile
    request = create_mock_request(user)
    
    # Try to access the patient dashboard
    response = patient_dashboard(request)
    print("Response status code:", response.status_code)
    print("Redirected to:", response.url if hasattr(response, 'url') else 'No redirect')
except Exception as e:
    print("Error:", str(e))

print("\nTesting with a patient user...")
try:
    user = User.objects.get(username='Sonu kumar')  # This user is a patient
    request = create_mock_request(user)
    
    # Try to access the patient dashboard
    response = patient_dashboard(request)
    print("Response status code:", response.status_code)
    print("Redirected to:", response.url if hasattr(response, 'url') else 'No redirect')
except Exception as e:
    print("Error:", str(e))