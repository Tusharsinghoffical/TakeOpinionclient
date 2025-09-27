import os
import django
from django.conf import settings

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'takeopinion.settings')
django.setup()

print("Testing that the models can be imported correctly in Django context...")

# Test the specific imports that were causing issues
try:
    from treatments.models import TreatmentCategory
    print("✓ TreatmentCategory imported successfully")
except Exception as e:
    print(f"✗ Error importing TreatmentCategory: {e}")

try:
    from core.models import State
    print("✓ State imported successfully")
except Exception as e:
    print(f"✗ Error importing State: {e}")

try:
    from treatments.models import Treatment
    print("✓ Treatment imported successfully")
except Exception as e:
    print(f"✗ Error importing Treatment: {e}")

try:
    from core.models import Country
    print("✓ Country imported successfully")
except Exception as e:
    print(f"✗ Error importing Country: {e}")

try:
    from doctors.models import Doctor
    print("✓ Doctor imported successfully")
except Exception as e:
    print(f"✗ Error importing Doctor: {e}")

try:
    from hospitals.models import Hospital
    print("✓ Hospital imported successfully")
except Exception as e:
    print(f"✗ Error importing Hospital: {e}")

# Test that the views can be imported (this was the original issue)
try:
    from accounts.views import admin_add_treatment, admin_add_hospital, admin_add_doctor
    print("✓ Admin views imported successfully")
    
    # Check if the source code contains the references to the models
    import inspect
    treatment_source = inspect.getsource(admin_add_treatment)
    hospital_source = inspect.getsource(admin_add_hospital)
    
    if 'TreatmentCategory' in treatment_source:
        print("✓ TreatmentCategory reference found in admin_add_treatment view")
    else:
        print("✗ TreatmentCategory reference NOT found in admin_add_treatment view")
        
    if 'State' in hospital_source:
        print("✓ State reference found in admin_add_hospital view")
    else:
        print("✗ State reference NOT found in admin_add_hospital view")
        
except Exception as e:
    print(f"✗ Error importing admin views: {e}")

print("\nTest completed. If all checks are ✓, then the original import errors should be resolved.")