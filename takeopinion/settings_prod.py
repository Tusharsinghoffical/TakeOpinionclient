import os
from pathlib import Path
import dj_database_url
from typing import Any, Dict

BASE_DIR = Path(__file__).resolve().parent.parent

from .settings import *

SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-0ylyg79(e+@2pv!zii$p1f^rc+@ifn&3&+1emsjgx%oti6^=0_')
DEBUG = False

ALLOWED_HOSTS = [
    'takeopinionclient.onrender.com',
    'takeopinionclientproject.onrender.com',
    '.onrender.com',
    'localhost',
    '127.0.0.1',
]

allowed_hosts_env = os.environ.get('ALLOWED_HOSTS')
if allowed_hosts_env:
    env_hosts = [h.strip() for h in allowed_hosts_env.split(',') if h.strip()]
    ALLOWED_HOSTS = list(dict.fromkeys(ALLOWED_HOSTS + env_hosts))

# ── Middleware (clean — no duplicates) ────────────────────────────────────────
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'core.middleware.LoginRequiredMiddleware',
    # AutoPatientLoginMiddleware intentionally removed — site is fully public
]

# ── Database ──────────────────────────────────────────────────────────────────
DATABASES: Dict[str, Any] = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

database_url = os.environ.get('DATABASE_URL')
if database_url:
    DATABASES['default'] = dj_database_url.parse(database_url)

# ── Static files ──────────────────────────────────────────────────────────────
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

# Use simple storage to avoid manifest hash issues on Render
STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'

WHITENOISE_USE_FINDERS = True
WHITENOISE_AUTOREFRESH = True
WHITENOISE_MANIFEST_STRICT = False
WHITENOISE_ALLOW_ALL_ORIGINS = True
WHITENOISE_SKIP_COMPRESS_EXTENSIONS = [
    'jpg', 'jpeg', 'png', 'gif', 'webp',
    'zip', 'gz', 'tgz', 'bz2', 'tbz', 'xz', 'br',
    'woff', 'woff2',
]

# ── Media ─────────────────────────────────────────────────────────────────────
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# ── Security headers ──────────────────────────────────────────────────────────
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'SAMEORIGIN'

# Keep cookies non-secure so the site works on HTTP Render free tier
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False

# ── Logging ───────────────────────────────────────────────────────────────────
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {'class': 'logging.StreamHandler'},
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