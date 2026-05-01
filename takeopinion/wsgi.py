"""
WSGI config for takeopinion project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

# Use the DJANGO_SETTINGS_MODULE environment variable if set, otherwise default to takeopinion.settings_prod for production
settings_module = os.environ.get("DJANGO_SETTINGS_MODULE", "takeopinion.settings_prod")

# Debug: Print the settings module being used
print(f"wsgi.py: Using DJANGO_SETTINGS_MODULE: {settings_module}")

# Check if the module name has been truncated and fix it
if settings_module.startswith("akeopinion."):
    corrected_module = "t" + settings_module
    print(f"wsgi.py: Correcting truncated module name from {settings_module} to {corrected_module}")
    os.environ["DJANGO_SETTINGS_MODULE"] = corrected_module
    settings_module = corrected_module

os.environ.setdefault("DJANGO_SETTINGS_MODULE", settings_module)

application = get_wsgi_application()