import os
import django
from django.conf import settings

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'takeopinion.settings')
django.setup()

# Test the specific views that were having issues
try:
    from accounts.views import admin_add_treatment, admin_add_hospital, admin_add_doctor
    print("All admin views imported successfully")
    
    # Test that the models are accessible within the views
    import inspect
    treatment_source = inspect.getsource(admin_add_treatment)
    hospital_source = inspect.getsource(admin_add_hospital)
    doctor_source = inspect.getsource(admin_add_doctor)
    
    # Check if TreatmentCategory and State are referenced in the source
    if 'TreatmentCategory' in treatment_source:
        print("TreatmentCategory reference found in admin_add_treatment")
    else:
        print("WARNING: TreatmentCategory reference NOT found in admin_add_treatment")
        
    if 'State' in hospital_source:
        print("State reference found in admin_add_hospital")
    else:
        print("WARNING: State reference NOT found in admin_add_hospital")
        
except Exception as e:
    print(f"Error importing admin views: {e}")
    import traceback
    traceback.print_exc()