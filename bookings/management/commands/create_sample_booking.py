from django.core.management.base import BaseCommand
from bookings.models import Booking
from treatments.models import Treatment
from doctors.models import Doctor
from hospitals.models import Hospital
from accounts.models import UserProfile
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Create a sample booking for testing'

    def handle(self, *args, **options):
        # Get required objects
        treatment = Treatment._default_manager.first()
        doctor = Doctor._default_manager.first()
        hospital = Hospital._default_manager.first()
        patient_user = User._default_manager.get(username='tusharsinghkumar0')
        patient = patient_user.userprofile

        # Create booking
        booking = Booking(
            treatment=treatment,
            preferred_doctor=doctor,
            preferred_hospital=hospital,
            patient=patient,
            amount=treatment.starting_price,
            status='confirmed'
        )
        booking.save()

        self.stdout.write(
            f'Successfully created booking #{booking.id} for {treatment.name}'
        )