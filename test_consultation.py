import os
import django
from datetime import datetime

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'takeopinion.settings')
django.setup()

from bookings.models import Booking
from doctors.models import Doctor
from treatments.models import Treatment
from accounts.models import UserProfile
from django.contrib.auth.models import User

def test_consultation_booking():
    # Get a doctor for testing
    doctor = Doctor.objects.first()
    if not doctor:
        print("No doctors found in the database.")
        return
    
    # Get a user for testing
    user = User.objects.first()
    if not user:
        print("No users found in the database.")
        return
    
    # Get or create user profile
    try:
        user_profile = user.userprofile
    except UserProfile.DoesNotExist:
        user_profile = UserProfile.objects.create(
            user=user,
            user_type='patient'
        )
    
    # Get or create a treatment
    treatment, created = Treatment.objects.get_or_create(
        name="General Consultation",
        defaults={
            'description': "General medical consultation",
            'starting_price': 50.00,
            'category_id': 1  # Assuming there's at least one category
        }
    )
    
    # Create a booking
    booking = Booking.objects.create(
        treatment=treatment,
        preferred_doctor=doctor,
        patient=user_profile,
        preferred_date=datetime.now().date(),
        amount=50.00,
        status='pending'
    )
    
    print(f"Created test booking: {booking}")
    print(f"Doctor: {doctor.name}")
    print(f"Patient: {user.username}")
    print(f"Treatment: {treatment.name}")
    print(f"Amount: ${booking.amount}")

if __name__ == '__main__':
    test_consultation_booking()