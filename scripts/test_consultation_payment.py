"""
Test script to verify consultation payment with Google Meet link functionality
"""
import os
import django
import uuid
from django.utils.text import slugify

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'takeopinion.settings')
django.setup()

from bookings.models import Booking
from treatments.models import Treatment, TreatmentCategory
from doctors.models import Doctor
from accounts.models import UserProfile
from django.contrib.auth.models import User

def test_consultation_payment_flow():
    print("Testing consultation payment flow with Google Meet link...")
    
    # Generate a unique username
    unique_id = uuid.uuid4().hex[:8]
    username = f'testuser_{unique_id}'
    
    # Create a test user
    user = User(
        username=username,
        email=f'test_{unique_id}@example.com'
    )
    user.set_password('testpass123')
    user.save()
    
    # Create a user profile
    user_profile = UserProfile(
        user=user,
        user_type='patient'
    )
    user_profile.save()
    
    # Create a treatment category with unique slug
    category = TreatmentCategory(
        name=f'Test Category {unique_id}',
        type='medical'
    )
    category.slug = slugify(category.name)
    category.save()
    
    # Create a test treatment
    treatment = Treatment(
        name=f'Test Treatment {unique_id}',
        description='Test treatment for consultation',
        starting_price=50.00,
        category=category
    )
    treatment.slug = slugify(treatment.name)
    treatment.save()
    
    # Create a test doctor
    doctor = Doctor(
        name=f'Dr. Test Doctor {unique_id}',
        specialization='Test Specialization'
    )
    doctor.slug = slugify(doctor.name)
    doctor.save()
    
    # Create a test booking with Google Meet link
    meet_link = f"https://meet.google.com/{uuid.uuid4().hex[:3]}-{uuid.uuid4().hex[:4]}-{uuid.uuid4().hex[:3]}"
    booking = Booking(
        treatment=treatment,
        preferred_doctor=doctor,
        patient=user_profile,
        status='pending',
        google_meet_link=meet_link,
        preferred_date='2025-12-01'
    )
    booking.save()
    
    print(f"Created consultation booking #{booking.id}")
    print(f"Google Meet link: {booking.google_meet_link}")
    
    # Verify the booking has the meet link
    assert booking.google_meet_link == meet_link
    assert booking.preferred_doctor is not None
    
    print("Consultation booking with Google Meet link created successfully!")
    
    # Clean up test data
    booking.delete()
    doctor.delete()
    treatment.delete()
    category.delete()
    user_profile.delete()
    user.delete()
    
    print("Test completed successfully!")

if __name__ == "__main__":
    test_consultation_payment_flow()