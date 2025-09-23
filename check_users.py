import os
import django

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'takeopinion.settings')
django.setup()

from django.contrib.auth.models import User
from accounts.models import UserProfile, PatientProfile

# Get all users
users = User.objects.all()

print("Users in the system:")
for user in users:
    print(f"- Username: {user.username}, Email: {user.email}")
    
    # Check if user has a profile
    try:
        profile = user.userprofile
        print(f"  Has profile: Yes, Type: {profile.user_type}")
        
        # Check if patient has patient details
        if profile.user_type == 'patient':
            try:
                patient_details = profile.patient_details
                print(f"  Has patient details: Yes")
            except:
                print(f"  Has patient details: No")
    except:
        print(f"  Has profile: No")

print("\nUser profiles count:", UserProfile.objects.count())
print("Patient profiles count:", PatientProfile.objects.count())