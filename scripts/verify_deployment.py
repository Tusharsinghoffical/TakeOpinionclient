#!/usr/bin/env python
"""
Deployment verification script for TakeOpinion
This script checks all critical components before deployment to Render
"""

import os
import sys
import django
from django.core.management import execute_from_command_line

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'takeopinion.settings_prod')
django.setup()

def check_python_version():
    """Check Python version compatibility"""
    print("Checking Python version...")
    version = sys.version_info
    if version.major == 3 and version.minor >= 8:
        print(f"✓ Python {sys.version}")
        return True
    else:
        print(f"✗ Python version too old: {sys.version}")
        return False

def check_required_packages():
    """Check if all required packages are installed"""
    print("\nChecking required packages...")
    required_packages = [
        'django',
        'gunicorn',
        'whitenoise',
        'PIL',  # Pillow
        'psycopg2',
        'dj_database_url'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            if package == 'PIL':
                import PIL
                print(f"✓ Pillow (PIL) {PIL.__version__}")
            else:
                __import__(package)
                print(f"✓ {package}")
        except ImportError:
            missing_packages.append(package)
            print(f"✗ {package} not found")
    
    return len(missing_packages) == 0

def check_django_settings():
    """Check Django settings configuration"""
    print("\nChecking Django settings...")
    try:
        from django.conf import settings
        
        # Check DEBUG setting
        if not settings.DEBUG:
            print("✓ DEBUG = False (production mode)")
        else:
            print("⚠ DEBUG = True (development mode)")
        
        # Check SECRET_KEY
        if settings.SECRET_KEY and len(settings.SECRET_KEY) > 10:
            print("✓ SECRET_KEY configured")
        else:
            print("⚠ SECRET_KEY not properly configured")
        
        # Check ALLOWED_HOSTS
        if settings.ALLOWED_HOSTS:
            print(f"✓ ALLOWED_HOSTS configured: {settings.ALLOWED_HOSTS[:3]}...")
        else:
            print("✗ ALLOWED_HOSTS not configured")
        
        # Check database configuration
        if settings.DATABASES and 'default' in settings.DATABASES:
            db_engine = settings.DATABASES['default'].get('ENGINE', '')
            if 'sqlite' in db_engine:
                print("⚠ Using SQLite database (will use PostgreSQL in production)")
            elif 'postgresql' in db_engine:
                print("✓ Using PostgreSQL database")
            else:
                print(f"? Database engine: {db_engine}")
        else:
            print("✗ Database not configured")
        
        # Check static files
        if settings.STATIC_ROOT:
            print(f"✓ STATIC_ROOT: {settings.STATIC_ROOT}")
        else:
            print("✗ STATIC_ROOT not configured")
        
        if settings.STATIC_URL:
            print(f"✓ STATIC_URL: {settings.STATIC_URL}")
        else:
            print("✗ STATIC_URL not configured")
        
        # Check media files
        if settings.MEDIA_ROOT:
            print(f"✓ MEDIA_ROOT: {settings.MEDIA_ROOT}")
        else:
            print("✗ MEDIA_ROOT not configured")
        
        if settings.MEDIA_URL:
            print(f"✓ MEDIA_URL: {settings.MEDIA_URL}")
        else:
            print("✗ MEDIA_URL not configured")
        
        return True
    except Exception as e:
        print(f"✗ Error checking Django settings: {e}")
        return False

def check_static_files():
    """Check static files configuration"""
    print("\nChecking static files...")
    try:
        from django.conf import settings
        from django.contrib.staticfiles import finders
        
        # Check if staticfiles app is installed
        if 'django.contrib.staticfiles' in settings.INSTALLED_APPS:
            print("✓ staticfiles app installed")
        else:
            print("✗ staticfiles app not installed")
        
        # Check static directories
        if settings.STATICFILES_DIRS:
            print(f"✓ STATICFILES_DIRS: {len(settings.STATICFILES_DIRS)} directories")
        else:
            print("✓ No additional static directories (this is fine)")
        
        # Check static files storage
        if hasattr(settings, 'STATICFILES_STORAGE'):
            print(f"✓ STATICFILES_STORAGE: {settings.STATICFILES_STORAGE}")
        else:
            print("✗ STATICFILES_STORAGE not configured")
        
        return True
    except Exception as e:
        print(f"✗ Error checking static files: {e}")
        return False

def check_media_files():
    """Check media files configuration"""
    print("\nChecking media files...")
    try:
        from django.conf import settings
        
        if settings.MEDIA_ROOT:
            media_root = settings.MEDIA_ROOT
            if os.path.exists(media_root):
                print(f"✓ MEDIA_ROOT exists: {media_root}")
                # Count files in media directory
                try:
                    file_count = sum(len(files) for _, _, files in os.walk(media_root))
                    print(f"✓ Media directory contains {file_count} files")
                except:
                    print("? Could not count media files")
            else:
                print(f"✓ MEDIA_ROOT configured (will be created on upload): {media_root}")
        else:
            print("✗ MEDIA_ROOT not configured")
        
        if settings.MEDIA_URL:
            print(f"✓ MEDIA_URL: {settings.MEDIA_URL}")
        else:
            print("✗ MEDIA_URL not configured")
        
        return True
    except Exception as e:
        print(f"✗ Error checking media files: {e}")
        return False

def check_database():
    """Check database connectivity"""
    print("\nChecking database connectivity...")
    try:
        from django.db import connection
        from django.db.utils import OperationalError
        
        # Try to connect to database
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
            if result and result[0] == 1:
                print("✓ Database connection successful")
            else:
                print("✗ Unexpected database response")
        
        # Check if tables exist
        try:
            table_names = connection.introspection.table_names()
            print(f"✓ Database contains {len(table_names)} tables")
        except:
            print("? Could not introspect database tables")
        
        return True
    except OperationalError as e:
        print(f"✗ Database connection failed: {e}")
        return False
    except Exception as e:
        print(f"✗ Error checking database: {e}")
        return False

def check_migrations():
    """Check if migrations are up to date"""
    print("\nChecking migrations...")
    try:
        from django.core.management import execute_from_command_line
        from io import StringIO
        import sys
        
        # Capture output from showmigrations
        old_stdout = sys.stdout
        sys.stdout = mystdout = StringIO()
        
        try:
            execute_from_command_line(['manage.py', 'showmigrations', '--plan'])
            sys.stdout = old_stdout
            output = mystdout.getvalue()
            
            if '[ ]' in output:
                print("⚠ Some migrations are not applied")
                # Count unapplied migrations
                unapplied = output.count('[ ]')
                print(f"  {unapplied} migrations need to be applied")
            else:
                print("✓ All migrations are applied")
        except Exception as e:
            sys.stdout = old_stdout
            print(f"? Could not check migrations: {e}")
        
        return True
    except Exception as e:
        print(f"✗ Error checking migrations: {e}")
        return False

def check_pillow():
    """Check Pillow installation and functionality"""
    print("\nChecking Pillow...")
    try:
        from PIL import Image, ImageDraw
        print(f"✓ Pillow {Image.__version__} installed")
        
        # Test basic functionality
        img = Image.new('RGB', (100, 100), color='red')
        draw = ImageDraw.Draw(img)
        draw.text((10, 10), "Test", fill='white')
        print("✓ Pillow image creation works")
        
        return True
    except Exception as e:
        print(f"✗ Pillow error: {e}")
        return False

def main():
    """Main verification function"""
    print("=== TakeOpinion Deployment Verification ===\n")
    
    checks = [
        ("Python Version", check_python_version),
        ("Required Packages", check_required_packages),
        ("Django Settings", check_django_settings),
        ("Static Files", check_static_files),
        ("Media Files", check_media_files),
        ("Database", check_database),
        ("Migrations", check_migrations),
        ("Pillow", check_pillow),
    ]
    
    results = []
    for check_name, check_func in checks:
        try:
            result = check_func()
            results.append((check_name, result))
        except Exception as e:
            print(f"✗ {check_name} check failed with exception: {e}")
            results.append((check_name, False))
    
    print("\n=== Summary ===")
    passed = 0
    total = len(results)
    
    for check_name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {check_name}")
        if result:
            passed += 1
    
    print(f"\n{passed}/{total} checks passed")
    
    if passed == total:
        print("\n🎉 All checks passed! Ready for deployment to Render.")
        return 0
    else:
        print(f"\n⚠ {total - passed} checks failed. Please fix issues before deployment.")
        return 1

if __name__ == '__main__':
    sys.exit(main())