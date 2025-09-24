# TakeOpinion - Render Deployment Setup

This repository contains a complete Django application ready for deployment on Render.com.

## Deployment Files

All necessary files for deployment have been created/updated:

1. `render.yaml` - Render deployment configuration
2. `takeopinion/settings_prod.py` - Production Django settings
3. `build.sh` - Build script for Render deployment
4. `RENDER_DEPLOYMENT_GUIDE.md` - Detailed deployment instructions
5. `DEPLOYMENT_SUMMARY.md` - Summary of all deployment configurations
6. `verify_deployment.py` - Deployment verification script
7. `check_server.py` - Application health check script

## Deployment Instructions

### Prerequisites
1. A Render account (https://render.com)
2. This repository connected to your Render account

### Steps
1. Go to your Render Dashboard
2. Click "New" and select "Web Service"
3. Connect your repository
4. Render will automatically detect this is a Python application
5. Confirm the following settings:
   - **Build Command**: `./build.sh`
   - **Start Command**: `gunicorn --bind 0.0.0.0:$PORT takeopinion.wsgi:application`
6. Set environment variables (Render will set most automatically):
   - `DJANGO_SETTINGS_MODULE=takeopinion.settings_prod`
   - `SECRET_KEY` (will be auto-generated)
   - `DEBUG=False`
7. Click "Create Web Service"

### Post-Deployment
1. After deployment completes, open a shell in Render dashboard
2. Run migrations: `python manage.py migrate`
3. (Optional) Create superuser: `python manage.py createsuperuser`

## Local Development

To run locally:
1. Create a virtual environment: `python -m venv venv`
2. Activate it: `venv\Scripts\activate` (Windows) or `source venv/bin/activate` (Mac/Linux)
3. Install dependencies: `pip install -r requirements.txt`
4. Run migrations: `python manage.py migrate`
5. Start server: `python manage.py runserver`

## Support

For deployment issues:
1. Check Render logs in the dashboard
2. Refer to `RENDER_DEPLOYMENT_GUIDE.md` for detailed instructions
3. Contact support if needed

The application is now ready for deployment on Render!