"""
Production settings for TakeOpinion project.

This file extends the base settings with production-specific configurations.
"""

import os
from .settings import *

# SECURITY WARNING: keep the secret key used in production secret!
# In production, this should be set as an environment variable
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-0ylyg79(e+@2pv!zii$p1f^rc+@ifn&3&+1emsjgx%oti6^=0_')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# Allow all hosts in production (you should specify your actual domain in production)
ALLOWED_HOSTS = ['*']

# Database configuration for production (using PostgreSQL as an example)
# In production, these should be set as environment variables
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',  # You should use PostgreSQL or MySQL in production
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATIC_URL = '/static/'

# Media files (user uploads)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Security settings for production
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_SSL_REDIRECT = True  # Only if you're using HTTPS (recommended)

# Session settings
SESSION_COOKIE_SECURE = True  # Only if you're using HTTPS
CSRF_COOKIE_SECURE = True     # Only if you're using HTTPS

# Logging configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'django.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}