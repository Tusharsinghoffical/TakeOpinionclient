# Deployment to Render

This document explains how to deploy the TakeOpinion application to Render with all data preserved.

## Prerequisites

1. A Render account (https://render.com)
2. Python 3.11+ installed locally

## Deployment Process

### 1. Prepare Data for Deployment

The application automatically exports and imports data during deployment:

```bash
# Export current data (done automatically by deploy script)
python export_data.py

# This creates JSON fixtures in the `fixtures` directory
```

### 2. Deploy to Render

1. Go to your Render dashboard
2. Click "New" → "Web Service"
3. Configure your deployment package
4. Configure the service:
   - **Name**: takeopinion (or your preferred name)
   - **Environment**: Python
   - **Build Command**: `./build.sh`
   - **Start Command**: `gunicorn --bind 0.0.0.0:$PORT takeopinion.wsgi:application`
   - **Branch**: main

5. Add Environment Variables:
   ```
   DJANGO_SETTINGS_MODULE=takeopinion.settings_prod
   SECRET_KEY=your-secret-key-here (or let Render auto-generate)
   DEBUG=False
   ALLOWED_HOSTS=.onrender.com,your-app-name.onrender.com
   ```

6. Click "Create Web Service"

### 3. Deployment Process Details

The `build.sh` script automatically:
1. Installs dependencies
2. Runs database migrations
3. Imports all data from fixtures
4. Collects static files

### 4. Data Preservation

All existing data (doctors, hospitals, treatments, bookings, etc.) will be preserved during deployment because:
- Data is exported to JSON fixtures
- Fixtures are included in the deployment package
- During deployment, data is automatically imported from fixtures

### 5. Post-Deployment

After deployment completes:
1. Visit your Render URL to verify the application is working
2. Create a superuser account through the Render dashboard shell
3. Log in to the admin dashboard to manage content
4. Test key functionality like booking and search

## Troubleshooting

If you encounter issues during deployment:

1. **Build Failures**: Check the build logs for dependency issues
2. **Application Crashes**: Check the application logs for runtime errors
3. **Data Import Issues**: Verify that all JSON fixtures are present
4. **Static Files Not Found**: Check that the build process completed successfully

## Support

For deployment assistance, refer to the main deployment guide or contact Render support.