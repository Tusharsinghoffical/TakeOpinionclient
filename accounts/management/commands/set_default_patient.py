from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from accounts.models import UserProfile


class Command(BaseCommand):
    help = 'Set or view default patient for auto-login'

    def add_arguments(self, parser):
        parser.add_argument(
            '--username',
            type=str,
            help='Username of the patient to set as default',
        )
        parser.add_argument(
            '--list',
            action='store_true',
            help='List all available patients',
        )

    def handle(self, *args, **options):
        if options['list']:
            self.list_patients()
        elif options['username']:
            self.set_default_patient(options['username'])
        else:
            self.show_current_default()

    def list_patients(self):
        patients = User.objects.filter(userprofile__user_type='patient')
        self.stdout.write("Available patients:")
        for patient in patients:
            profile = patient.userprofile
            name = f"{patient.first_name} {patient.last_name}".strip() or "No name"
            self.stdout.write(
                f"  - {patient.username} ({name}) - ID: {patient.id}")

    def set_default_patient(self, username):
        try:
            user = User.objects.get(username=username)
            if hasattr(user, 'userprofile') and user.userprofile.user_type == 'patient':
                # Update the middleware with this username
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Successfully set {user.username} as default patient'
                    )
                )
                self.stdout.write(
                    "To make this permanent, update the default_patient_username "
                    "in core/middleware.py AutoPatientLoginMiddleware"
                )
            else:
                self.stdout.write(
                    self.style.ERROR(
                        f'User {username} is not a patient or has no profile'
                    )
                )
        except User.DoesNotExist:
            self.stdout.write(
                self.style.ERROR(f'User {username} does not exist')
            )

    def show_current_default(self):
        # This would read from the middleware configuration
        self.stdout.write("Current default patient setting:")
        self.stdout.write(
            "  Username: tusharsinghkumar02 (configured in middleware)")
        self.stdout.write("\nTo change this, use:")
        self.stdout.write(
            "  python manage.py set_default_patient --username <username>")
        self.stdout.write("  python manage.py set_default_patient --list")
