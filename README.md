# TakeOpinion - Medical Tourism Platform

TakeOpinion is a comprehensive medical tourism platform that connects patients with healthcare providers worldwide.

## Project Overview

This Django-based web application provides a complete solution for medical tourism, including:
- Hospital and doctor listings
- Treatment information and pricing
- Appointment booking system
- Patient reviews and ratings
- Blog content management
- Payment processing

## Deployment Instructions

### For Render Deployment

1. Fork this repository to your GitHub account
2. Create a new Web Service on Render
3. Connect your GitHub repository
4. Configure the service with:
   - **Build Command**: `./build.sh`
   - **Start Command**: `gunicorn --bind 0.0.0.0:$PORT takeopinion.wsgi:application`
   - **Environment Variables**:
     ```
     DJANGO_SETTINGS_MODULE=takeopinion.settings_prod
     SECRET_KEY=your-secret-key-here
     DEBUG=False
     ALLOWED_HOSTS=.onrender.com,your-app-name.onrender.com
     ```

### Important Note About Start Command

If you encounter an error like `bash: line 1: unicorn: command not found`, this means Render is trying to use `unicorn` instead of `gunicorn`. This can happen if the Start Command was manually overridden in the Render dashboard. To fix this:

1. Go to your Render dashboard
2. Click on your service
3. Go to "Settings" tab
4. Find "Start Command" and ensure it's set to:
   ```
   gunicorn --bind 0.0.0.0:$PORT takeopinion.wsgi:application
   ```

### For Local Development (Windows)

Due to compatibility issues with Gunicorn on Windows, use the Django development server:

```bash
python manage.py runserver
```

Or use the provided startup script:
```bash
python start_server.py
```

## Data Management

The application includes comprehensive data fixtures for:
- Hospitals and doctors
- Medical treatments
- Patient bookings
- User reviews

Data is automatically imported during the build process on Render.

## Environment Variables

- `DJANGO_SETTINGS_MODULE`: Django settings module (default: takeopinion.settings for development, takeopinion.settings_prod for production)
- `SECRET_KEY`: Django secret key
- `DEBUG`: Debug mode (True/False)
- `ALLOWED_HOSTS`: Comma-separated list of allowed hosts
- `DATABASE_URL`: Database connection URL (optional, for PostgreSQL)

## Troubleshooting

### Gunicorn Issues on Windows

Gunicorn is not compatible with Windows due to its dependency on the `fcntl` module. For local development on Windows, always use Django's built-in development server.

### Data Import Issues

If you encounter foreign key constraint errors during data import, ensure that all related objects are imported in the correct order. The import script handles this automatically.

The application uses `comprehensive_medical_data.json` for complete data that includes both User and UserProfile objects to avoid foreign key issues.

### Start Command Issues

If Render is trying to use `unicorn` instead of `gunicorn`, check your service settings in the Render dashboard and ensure the Start Command is correctly set.

## Support

For deployment assistance, contact the development team.