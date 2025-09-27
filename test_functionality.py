import os
import django
from django.conf import settings

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'takeopinion.settings')
django.setup()

# Test the specific functionality that was failing
try:
    from treatments.models import TreatmentCategory
    from core.models import State, Country
    print("Models imported successfully")
    
    # Test creating a TreatmentCategory
    category, created = TreatmentCategory.objects.get_or_create(
        name="Test Category",
        defaults={'type': 'medical'}
    )
    print(f"Created/Found TreatmentCategory: {category.name}")
    
    # Test creating a State
    country, created = Country.objects.get_or_create(
        name="Test Country",
        code="TC"
    )
    state, created = State.objects.get_or_create(
        country=country,
        name="Test State"
    )
    print(f"Created/Found State: {state.name}")
    
    print("All tests passed successfully!")
    
except Exception as e:
    print(f"Error during testing: {e}")
    import traceback
    traceback.print_exc()