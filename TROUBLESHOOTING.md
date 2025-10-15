# TakeOpinion Deployment Troubleshooting Guide

This guide helps resolve common issues encountered when deploying the TakeOpinion application to Render.

## Common Deployment Issues and Solutions

### 1. `unicorn: command not found` Error

**Problem**: Render is trying to run `unicorn` instead of `gunicorn`.

**Solution**:
1. Go to your Render dashboard
2. Click on your service
3. Go to "Settings" tab
4. Find "Start Command" and ensure it's set to:
   ```
   gunicorn --bind 0.0.0.0:$PORT takeopinion.wsgi:application
   ```

**Prevention**: Ensure your `render.yaml` file has the correct startCommand and that it hasn't been manually overridden in the Render dashboard.

### 2. Foreign Key Constraint Errors During Data Import

**Problem**: Error messages like "The row in table 'bookings_booking' with primary key '1' has an invalid foreign key: bookings_booking.patient_id contains a value '9' that does not have a corresponding value in accounts_userprofile.id."

**Solution**:
1. The application uses `comprehensive_medical_data.json` which contains complete User and UserProfile data
2. Ensure that `accounts_data.json` (which is incomplete) has been removed
3. Verify that the import script in `scripts/import_data.py` is using `comprehensive_medical_data.json`

**Prevention**: Always use the comprehensive data fixture that includes both User and UserProfile objects to maintain referential integrity.

### 3. Gunicorn Not Working on Windows

**Problem**: `ModuleNotFoundError: No module named 'fcntl'` when trying to run gunicorn locally.

**Solution**: 
- For local development on Windows, use Django's built-in development server:
  ```bash
  python manage.py runserver
  ```
- Or use the provided cross-platform startup script:
  ```bash
  python start_server.py
  ```

**Prevention**: Remember that gunicorn is only for production deployment on Linux/Render, not for local Windows development.

### 4. Static Files Not Loading

**Problem**: CSS, JavaScript, or images are not loading on the deployed site.

**Solution**:
1. Ensure the build script runs `python manage.py collectstatic`
2. Check that `STATIC_ROOT` is properly configured in `settings_prod.py`
3. Verify that Whitenoise is properly configured for serving static files

### 5. Database Migration Issues

**Problem**: Database errors or missing tables after deployment.

**Solution**:
1. Ensure the build script runs `python manage.py migrate`
2. Check that the database URL is properly configured with `DATABASE_URL` environment variable
3. For PostgreSQL, ensure `psycopg2-binary` is in `requirements.txt`

### 6. Environment Variable Issues

**Problem**: Application not working due to missing or incorrect environment variables.

**Required Environment Variables**:
```
DJANGO_SETTINGS_MODULE=takeopinion.settings_prod
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=.onrender.com,your-app-name.onrender.com
```

**Solution**:
1. Check that all required environment variables are set in the Render dashboard
2. Verify that `ALLOWED_HOSTS` includes your Render domain

### 7. Build Process Failures

**Problem**: Deployment fails during the build process.

**Solution**:
1. Check the build logs for specific error messages
2. Ensure all dependencies in `requirements.txt` are correct
3. Verify that `runtime.txt` specifies the correct Python version
4. Check that the build script (`build.sh`) has proper permissions

## Debugging Steps

### 1. Check Build Logs
- Go to your Render dashboard
- Click on your service
- Go to "Logs" tab
- Look for error messages during the build process

### 2. Check Application Logs
- Go to your Render dashboard
- Click on your service
- Go to "Logs" tab
- Look for error messages after deployment

### 3. Verify Configuration Files
- Check `render.yaml` for correct build and start commands
- Verify `requirements.txt` contains all necessary dependencies
- Ensure `runtime.txt` specifies the correct Python version

### 4. Test Locally
- Run the application locally to identify issues before deployment
- Use the same environment variables as in production
- Test the build script locally

## Contact Support

If you continue to experience issues:

1. Check the [Render troubleshooting documentation](https://render.com/docs/troubleshooting-deploys)
2. Review the error logs in your Render dashboard
3. Contact Render support with specific error messages
4. For application-specific issues, contact the development team