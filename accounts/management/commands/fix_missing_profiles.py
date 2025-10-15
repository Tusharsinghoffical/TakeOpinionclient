from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from accounts.models import UserProfile, PatientProfile, DoctorProfile

class Command(BaseCommand):
    help = 'Creates missing user profiles for existing users'

    def handle(self, *args, **options):
        users = User.objects.all()
        created_profiles = 0
        
        for user in users:
            # Check if user has a profile
            try:
                profile = user.userprofile
                self.stdout.write(f"User {user.username} already has a profile")
            except UserProfile.DoesNotExist:
                # Create a default profile for users without one
                # We'll assume they are patients by default
                profile = UserProfile.objects.create(
                    user=user,
                    user_type='patient'
                )
                # Also create the specific profile
                PatientProfile.objects.create(user_profile=profile)
                created_profiles += 1
                self.stdout.write(f"Created profile for user {user.username}")
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created {created_profiles} user profiles'
            )
        )