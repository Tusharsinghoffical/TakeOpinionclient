import os
import sys
import django

# Add the project directory to the Python path
sys.path.append("c:\\Users\\tusha\\Desktop\\Client 2")

# Set the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'takeopinion.settings')

# Setup Django
django.setup()

from hospitals.models import Hospital
from core.models import Country, State
from treatments.models import Treatment, TreatmentCategory

def populate_hospital_data():
    # Create or get country and state
    country, created = Country.objects.get_or_create(name="India", code="IN")
    if created:
        print(f"Created country: {country.name}")
    
    state, created = State.objects.get_or_create(name="Delhi", country=country)
    if created:
        print(f"Created state: {state.name}")
    
    # Create treatment categories
    medical_category, created = TreatmentCategory.objects.get_or_create(
        name="Medical Treatments",
        defaults={
            "slug": "medical-treatments",
            "type": "medical"
        }
    )
    if created:
        print(f"Created treatment category: {medical_category.name}")
    
    # Create or update Apollo Hospital
    hospital, created = Hospital.objects.get_or_create(
        name="Apollo Hospital",
        defaults={
            'city': 'Delhi',
            'address': '123 Medical Plaza',
            'about': 'Apollo Hospitals is a leading healthcare institution with state-of-the-art facilities and a commitment to providing exceptional patient care.',
            'rating': 4.5,
            'is_takeopinion_choice': True,
            'phone': '+91 11 2345 6789',
            'email': 'info@apollohospital.com',
            'website': 'https://www.apollohospitals.com',
            'established_year': 1983,
            'beds_count': 500,
            'staff_count': 1200,
            'departments_count': 35,
            'awards_count': 25,
            'jci_accredited': True,
            'nabh_accredited': True,
            'iso_certified': True,
            'country': country,
            'state': state
        }
    )
    
    if created:
        print(f"Created hospital: {hospital.name}")
    else:
        print(f"Hospital already exists: {hospital.name}")
        # Update the existing hospital with new information
        hospital.city = 'Delhi'
        hospital.address = '123 Medical Plaza'
        hospital.about = 'Apollo Hospitals is a leading healthcare institution with state-of-the-art facilities and a commitment to providing exceptional patient care.'
        hospital.rating = 4.5
        hospital.is_takeopinion_choice = True
        hospital.phone = '+91 11 2345 6789'
        hospital.email = 'info@apollohospital.com'
        hospital.website = 'https://www.apollohospitals.com'
        hospital.established_year = 1983
        hospital.beds_count = 500
        hospital.staff_count = 1200
        hospital.departments_count = 35
        hospital.awards_count = 25
        hospital.jci_accredited = True
        hospital.nabh_accredited = True
        hospital.iso_certified = True
        hospital.country = country
        hospital.state = state
        hospital.save()
        print(f"Updated hospital: {hospital.name}")
    
    # Create some sample treatments
    treatments_data = [
        {"name": "Knee Replacement", "slug": "knee-replacement"},
        {"name": "Rhinoplasty", "slug": "rhinoplasty"},
        {"name": "Panchakarma", "slug": "panchakarma"},
        {"name": "AIDS Treatment", "slug": "aids-treatment"},
        {"name": "Diabetes Management", "slug": "diabetes-management"}
    ]
    
    treatments = []
    for treatment_data in treatments_data:
        treatment, created = Treatment.objects.get_or_create(
            name=treatment_data["name"],
            defaults={
                "slug": treatment_data["slug"],
                "category": medical_category
            }
        )
        treatments.append(treatment)
        if created:
            print(f"Created treatment: {treatment.name}")
    
    # Associate treatments with hospital
    hospital.treatments.set(treatments)
    print(f"Associated {len(treatments)} treatments with {hospital.name}")
    
    print("\nHospital data population completed!")
    print(f"You can now manage all hospital details through the Django admin panel.")
    print(f"Access: http://127.0.0.1:8000/admin/")

if __name__ == "__main__":
    populate_hospital_data()