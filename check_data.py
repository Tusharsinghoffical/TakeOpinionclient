import os
import django

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'takeopinion.settings')
django.setup()

from treatments.models import Treatment
from doctors.models import Doctor

print("Checking data...")
print(f"Total treatments: {Treatment.objects.count()}")
print(f"Total doctors: {Doctor.objects.count()}")

# Check first few treatments and their doctors
treatments = Treatment.objects.all()[:5]
for t in treatments:
    doctor_count = t.doctors.count()
    print(f"Treatment: {t.name}, Doctors: {doctor_count}")