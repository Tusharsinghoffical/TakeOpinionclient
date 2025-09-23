import os
import django

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'takeopinion.settings')
django.setup()

from django.contrib.auth.models import User
from accounts.models import UserProfile, PatientProfile
from accounts.views import patient_dashboard

print("Testing patient dashboard view...")

# Test with a user that has a complete profile
print("\nTesting with user that has complete profile...")
try:
    # Create a test user with complete profile
    user, created = User.objects.get_or_create(username='test_user_complete')
    if created:
        user.set_password('testpass')
        user.save()
    
    # Create user profile
    user_profile, created = UserProfile.objects.get_or_create(
        user=user,
        user_type='patient'
    )
    
    # Create patient profile
    patient_profile, created = PatientProfile.objects.get_or_create(
        user_profile=user_profile
    )
    
    # Test the view function directly
    from django.test import RequestFactory
    from django.contrib.auth.models import AnonymousUser
    from django.contrib.sessions.middleware import SessionMiddleware
    from django.contrib.messages.middleware import MessageMiddleware
    
    factory = RequestFactory()
    request = factory.get('/accounts/patient/dashboard/')
    request.user = user
    
    # Add session
    from django.contrib.sessions.backends.db import SessionStore
    request.session = SessionStore()
    request.session.create()
    
    # Add messages
    from django.contrib.messages.storage.fallback import FallbackStorage
    messages = FallbackStorage(request)
    request._messages = messages
    
    # Try to access the patient dashboard
    response = patient_dashboard(request)
    print(f"Response status code: {response.status_code}")
    print("Test completed successfully!")
except Exception as e:
    print(f"Error: {str(e)}")
    import traceback
    traceback.print_exc()

print("\nTest completed!")