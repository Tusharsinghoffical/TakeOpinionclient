import os
import sys
import django

# Add the project directory to the Python path
sys.path.append("c:\\Users\\tusha\\Desktop\\Client 2")

# Set the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'takeopinion.settings')

# Setup Django
django.setup()

from doctors.models import Doctor
from hospitals.models import Hospital
from treatments.models import Treatment

def populate_doctor_data():
    # Get or create a hospital
    try:
        hospital = Hospital.objects.get(name="Apollo Hospital")
        print(f"Found hospital: {hospital.name}")
    except Hospital.DoesNotExist:
        print("Apollo Hospital not found. Please create a hospital first.")
        return
    
    # Create or update Dr. Arjun Mehta
    doctor, created = Doctor.objects.get_or_create(
        name="Dr. Arjun Mehta",
        defaults={
            'specialization': 'Orthopedic Surgeon',
            'about': 'Dr. Arjun Mehta is a highly qualified orthopedic surgeon with extensive experience in joint replacement and sports injury treatment. With over 12 years of practice, he has successfully treated numerous patients and contributed to advancing medical knowledge in his area of expertise.',
            'key_points': 'Expert in knee and hip replacement surgeries, Sports injury specialist, Patient-centered approach',
            'education': 'MBBS, MS Orthopedics',
            'experience_years': 12,
            'phone': '+91 98765 43210',
            'email': 'arjun.mehta@apollo.com',
            'website': 'https://www.apollohospitals.com/doctors/arjun-mehta',
            'rating': 4.8,
            'review_count': 120,
            'medical_license_number': 'MED123456789',
            'languages_spoken': 'English, Hindi, Marathi'
        }
    )
    
    if created:
        print(f"Created doctor: {doctor.name}")
    else:
        print(f"Doctor already exists: {doctor.name}")
        # Update the existing doctor with new information
        doctor.specialization = 'Orthopedic Surgeon'
        doctor.about = 'Dr. Arjun Mehta is a highly qualified orthopedic surgeon with extensive experience in joint replacement and sports injury treatment. With over 12 years of practice, he has successfully treated numerous patients and contributed to advancing medical knowledge in his area of expertise.'
        doctor.key_points = 'Expert in knee and hip replacement surgeries, Sports injury specialist, Patient-centered approach'
        doctor.education = 'MBBS, MS Orthopedics'
        doctor.experience_years = 12
        doctor.phone = '+91 98765 43210'
        doctor.email = 'arjun.mehta@apollo.com'
        doctor.website = 'https://www.apollohospitals.com/doctors/arjun-mehta'
        doctor.rating = 4.8
        doctor.review_count = 120
        doctor.medical_license_number = 'MED123456789'
        doctor.languages_spoken = 'English, Hindi, Marathi'
        doctor.save()
        print(f"Updated doctor: {doctor.name}")
    
    # Associate hospital with doctor
    doctor.hospitals.add(hospital)
    print(f"Associated {doctor.name} with {hospital.name}")
    
    # Get some treatments to associate with the doctor
    treatments = Treatment.objects.all()[:5]  # Get first 5 treatments
    if treatments:
        doctor.treatments.set(treatments)
        print(f"Associated {len(treatments)} treatments with {doctor.name}")
    
    print("\nDoctor data population completed!")
    print(f"You can now manage all doctor details through the Django admin panel.")
    print(f"Access: http://127.0.0.1:8000/admin/")

if __name__ == "__main__":
    populate_doctor_data()