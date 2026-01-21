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
# Default to SQLite for local development, but use PostgreSQL if DATABASE_URL is provided
DATABASES: Dict[str, Any] = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# If DATABASE_URL environment variable is provided, use it (for PostgreSQL on Render)
database_url = os.environ.get('DATABASE_URL')
if database_url:
    DATABASES['default'] = dj_database_url.parse(database_url)
else:
    print("WARNING: Using SQLite database. For production, set DATABASE_URL environment variable.")

# Static files (CSS, JavaScript, Images)
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'

# Additional directories containing static files
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

# Use WhiteNoise for static files with a more permissive storage
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# WhiteNoise settings
WHITENOISE_USE_FINDERS = True
WHITENOISE_AUTOREFRESH = True
WHITENOISE_MANIFEST_STRICT = False

# Add WhiteNoise middleware at the beginning to serve static files
# This ensures WhiteNoise handles static files before other middleware
MIDDLEWARE = [
    'whitenoise.middleware.WhiteNoiseMiddleware',  # WhiteNoise should be first
] + MIDDLEWARE

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
        'django.request': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
        'whitenoise': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}

# WhiteNoise configuration for serving media files
WHITENOISE_ALLOW_ALL_ORIGINS = True

# Additional WhiteNoise settings for better compatibility
WHITENOISE_SKIP_COMPRESS_EXTENSIONS = ['jpg', 'jpeg', 'png', 'gif', 'webp', 'zip', 'gz', 'tgz', 'bz2', 'tbz', 'xz', 'br', 'woff', 'woff2']