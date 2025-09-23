# Deployment Checklist

## Files and Directories Included

### Core Application Files
- All Django application code (accounts, blogs, bookings, core, doctors, feedbacks, hospitals, treatments)
- Settings and configuration files
- URL routing files
- Management commands

### Static Files
- CSS files in `static/css/`
- Image files in `static/images/`
- JavaScript files in `static/js/`
- All collected static files in `staticfiles/` directory

### Media Files
- User uploaded files directory `media/`

### Database
- SQLite database file `db.sqlite3` (contains all data)

### Templates
- All HTML templates in respective app directories
- Base templates

### Documentation
- README.md
- DEPLOYMENT.md
- All other markdown documentation files

### Configuration Files
- requirements.txt (dependencies)
- .gitignore

## Pre-deployment Tasks Completed

1. ✅ Collected all static files using `python manage.py collectstatic`
2. ✅ Created media directory for user uploads
3. ✅ Configured media file serving in settings.py
4. ✅ Cleaned up cache files (__pycache__ directories)
5. ✅ Removed .pyc files
6. ✅ Created requirements.txt with dependencies
7. ✅ Verified application runs without errors
8. ✅ Tested server startup

## Deployment Instructions

1. Clone or copy all files to the deployment server
2. Install dependencies: `pip install -r requirements.txt`
3. Run migrations if needed: `python manage.py migrate`
4. Collect static files: `python manage.py collectstatic --noinput`
5. Ensure media directory is writable
6. Start the server: `python manage.py runserver` or use a production server like Gunicorn

## Post-deployment Verification

1. ✅ All pages load correctly
2. ✅ Static files are served properly
3. ✅ Media files can be uploaded and accessed
4. ✅ Database queries work
5. ✅ User authentication functions
6. ✅ All forms submit correctly

## Notes

- The application uses SQLite database which is included in the deployment package
- Media files directory should be backed up regularly
- Static files are served by WhiteNoise in production
- For production deployment, consider using a proper web server like Nginx with Gunicorn