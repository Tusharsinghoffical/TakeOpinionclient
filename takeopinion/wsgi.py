"""
WSGI config for takeopinion project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

# Use the DJANGO_SETTINGS_MODULE environment variable if set, otherwise default to takeopinion.settings_prod for production
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "takeopinion.settings_prod")

application = get_wsgi_application()