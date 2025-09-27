import os
import sys
import django
from django.contrib.auth.models import User

# Setup Django environment
project_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(project_path)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'takeopinion.settings')
django.setup()

from django.utils import timezone
from datetime import datetime, timedelta
from accounts.models import UserProfile, PatientProfile, DoctorProfile
from treatments.models import TreatmentCategory, Treatment
from hospitals.models import Hospital
from doctors.models import Doctor
from bookings.models import Booking
from blogs.models import BlogPost
from core.models import Country, State

def create_sample_data():
    print("Creating sample data...")
    
    # Create countries and states
    print("Creating countries and states...")
    india, created = Country.objects.get_or_create(
        name="India",
        code="IN",
        defaults={"slug": "india"}
    )
    
    # Create admin user
    print("Creating admin user...")
    admin_user, created = User.objects.get_or_create(
        username="admin",
        defaults={
            "email": "admin@takeopinion.com",
            "first_name": "Admin",
            "last_name": "User"
        }
    )
    if created:
        admin_user.set_password("admin123")
        admin_user.is_staff = True
        admin_user.is_superuser = True
        admin_user.save()
    
    admin_profile, created = UserProfile.objects.get_or_create(
        user=admin_user,
        defaults={
            "user_type": "admin",
            "phone": "+91-9876543210",
            "address": "Admin Office, New Delhi",
            "city": "New Delhi"
        }
    )
    
    print("Sample data creation completed!")
    print("\nLogin credentials:")
    print("- Admin: admin / admin123")

if __name__ == "__main__":
    create_sample_data()