import os
import django
from django.conf import settings

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'takeopinion.settings')
django.setup()

# Test imports
try:
    from treatments.models import Treatment, TreatmentCategory
    print("Treatment and TreatmentCategory imported successfully")
except Exception as e:
    print(f"Error importing Treatment models: {e}")

try:
    from core.models import State
    print("State imported successfully")
except Exception as e:
    print(f"Error importing State model: {e}")

try:
    from accounts.views import admin_add_treatment, admin_add_hospital
    print("Admin views imported successfully")
except Exception as e:
    print(f"Error importing admin views: {e}")