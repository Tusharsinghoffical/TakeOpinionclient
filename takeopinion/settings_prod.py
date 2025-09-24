"""
Production settings for TakeOpinion project.

This file extends the base settings with production-specific configurations.
"""

import os
from pathlib import Path
import dj_database_url
from typing import Any, Dict

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Import base settings
from .settings import *

# Override base settings with production-specific values
# SECURITY WARNING: keep the secret key used in production secret!
# In production, this should be set as an environment variable
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-0ylyg79(e+@2pv!zii$p1f^rc+@ifn&3&+1emsjgx%oti6^=0_')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# Allow hosts - in production, specify your actual domain
ALLOWED_HOSTS = [
    'takeopinionclient.onrender.com',
    '.onrender.com',
    'localhost',
    '127.0.0.1'
]

# Process ALLOWED_HOSTS environment variable if provided
allowed_hosts_env = os.environ.get('ALLOWED_HOSTS')
if allowed_hosts_env:
    # Split the environment variable by comma and strip whitespace
    env_hosts = [host.strip() for host in allowed_hosts_env.split(',') if host.strip()]
    # Add environment hosts to our list
    ALLOWED_HOSTS.extend(env_hosts)
    # Remove duplicates while preserving order
    ALLOWED_HOSTS = list(dict.fromkeys(ALLOWED_HOSTS))

# Database configuration for production
# Using SQLite for now to avoid compatibility issues, but can be configured for PostgreSQL
DATABASES: Dict[str, Any] = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# If DATABASE_URL environment variable is provided, use it (for PostgreSQL)
if 'DATABASE_URL' in os.environ:
    DATABASES['default'] = dj_database_url.parse(os.environ['DATABASE_URL'])

# Static files (CSS, JavaScript, Images)
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'

# Additional directories containing static files
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

# Use WhiteNoise for static files with compressed storage
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Media files (user uploads)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Security settings for production
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# Session settings
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# Logging configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
            'propagate': False,
        },
    },
}