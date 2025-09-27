import os
import django
from django.conf import settings

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'takeopinion.settings')
django.setup()

from core.views import get_home_content
from django.http import HttpRequest

# Create a request object
req = HttpRequest()
req.method = 'GET'

# Call the function and print the result
try:
    response = get_home_content(req)
    print(f"Status: {response.status_code}")
    print(f"Content: {response.content}")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()