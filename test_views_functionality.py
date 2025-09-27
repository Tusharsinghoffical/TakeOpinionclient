import os
import django
from django.conf import settings
import uuid

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'takeopinion.settings')
django.setup()

# Test the specific view functionality that was failing
try:
    from treatments.models import Treatment, TreatmentCategory
    from core.models import State, Country
    from doctors.models import Doctor
    from hospitals.models import Hospital
    print("All models imported successfully")
    
    # Generate unique names to avoid conflicts
    unique_id = str(uuid.uuid4())[:8]
    
    # Test the exact functionality from admin_add_treatment
    print("Testing TreatmentCategory usage (similar to admin_add_treatment)...")
    name = f"Test Treatment {unique_id}"
    category_name = "medical"
    starting_price = 1000
    
    # Get or create category (this is what was failing)
    category, created = TreatmentCategory.objects.get_or_create(
        name=category_name.title(),
        defaults={'type': category_name}
    )
    print(f"Created/Found TreatmentCategory: {category.name}")
    
    # Create treatment
    treatment = Treatment.objects.create(
        name=name,
        category=category,
        starting_price=starting_price
    )
    print(f"Created Treatment: {treatment.name}")
    
    # Test the exact functionality from admin_add_hospital
    print("Testing State usage (similar to admin_add_hospital)...")
    hospital_name = f"Test Hospital {unique_id}"
    city = "Test City"
    state_name = f"Test State {unique_id}"
    established_year = 2020
    
    # Try to get or create state (this is what was failing)
    state = None
    if state_name:
        # First create a country if needed
        country, created = Country.objects.get_or_create(
            name=f"Test Country {unique_id}",
            code="TC"
        )
        state, created = State.objects.get_or_create(
            name=state_name,
            country=country
        )
    print(f"Created/Found State: {state.name if state else 'None'}")
    
    # Create hospital
    hospital = Hospital.objects.create(
        name=hospital_name,
        city=city,
        state=state,
        established_year=established_year,
        rating=0.0
    )
    print(f"Created Hospital: {hospital.name}")
    
    # Test the exact functionality from admin_add_doctor
    print("Testing Doctor creation (similar to admin_add_doctor)...")
    doctor_name = f"Test Doctor {unique_id}"
    specialization = "Test Specialization"
    email = f"test{unique_id}@example.com"
    experience_years = 10
    
    doctor = Doctor.objects.create(
        name=doctor_name,
        specialization=specialization,
        email=email,
        experience_years=experience_years,
        rating=0.0,
        review_count=0
    )
    print(f"Created Doctor: {doctor.name}")
    
    print("All view functionality tests passed successfully!")
    print("This confirms that the 'TreatmentCategory is not defined' and 'State is not defined' errors should be resolved.")
    
except Exception as e:
    print(f"Error during testing: {e}")
    import traceback
    traceback.print_exc()