from django.core.management.base import BaseCommand
from doctors.models import Doctor

class Command(BaseCommand):
    help = 'Add profile pictures to all doctors who don\'t have one'

    def handle(self, *args, **options):
        # Get all doctors without profile pictures
        doctors_without_pictures = Doctor.objects.filter(profile_picture='')  # type: ignore
        
        self.stdout.write(
            f'Found {doctors_without_pictures.count()} doctors without profile pictures'
        )
        
        # Add profile pictures using UI Avatars service
        for doctor in doctors_without_pictures:
            # Create a URL-safe name for the doctor
            name_parts = doctor.name.replace('Dr. ', '').replace('Dr ', '').strip().split()
            if len(name_parts) >= 2:
                # Use first name and last name
                name_param = f"{name_parts[0]}+{name_parts[-1]}"
            else:
                # Use just the first name or the whole name
                name_param = name_parts[0] if name_parts else doctor.name
            
            # Generate UI Avatars URL
            profile_picture_url = f"https://ui-avatars.com/api/?name={name_param}&background=0D8ABC&color=fff&size=256"
            
            # Update the doctor's profile picture
            doctor.profile_picture = profile_picture_url
            doctor.save()
            
            self.stdout.write(
                f'Added profile picture for {doctor.name}'
            )
        
        self.stdout.write(
            f'Successfully added profile pictures to {doctors_without_pictures.count()} doctors'
        )