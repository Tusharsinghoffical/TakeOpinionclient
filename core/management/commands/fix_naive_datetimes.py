from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
import datetime

class Command(BaseCommand):
    help = 'Fix naive datetime values in User.date_joined field'

    def handle(self, *args, **options):
        # Get all users and check for naive datetime values
        all_users = User.objects.all()
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Checking {all_users.count()} users for naive datetime values'
            )
        )
        
        fixed_count = 0
        for user in all_users:
            # Check if datetime is naive (has no timezone info)
            if user.date_joined.tzinfo is None:
                # Convert naive datetime to timezone-aware
                # Assume UTC timezone for naive datetimes
                aware_datetime = timezone.make_aware(user.date_joined, timezone.utc)
                user.date_joined = aware_datetime
                user.save(update_fields=['date_joined'])
                fixed_count += 1
                
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully fixed {fixed_count} user records'
            )
        )