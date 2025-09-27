# Deployment Guide for TakeOpinion

This guide explains how to deploy the TakeOpinion application to Render.

## Prerequisites

1. A Render account (https://render.com)
2. A GitHub account with the repository cloned
3. Basic knowledge of Django and web deployment

## Deploying to Render

### 1. Fork the Repository

First, fork this repository to your GitHub account.

### 2. Create a New Web Service on Render

1. Go to your Render dashboard
2. Click "New" and select "Web Service"
3. Connect your GitHub account and select your forked repository
4. Fill in the following settings:
   - Name: takeopinion
   - Environment: Python
   - Build Command: `./build.sh`
   - Start Command: `gunicorn --bind 0.0.0.0:$PORT takeopinion.wsgi:application`
   - Branch: main (or your default branch)

### 3. Add Environment Variables

In the "Environment Variables" section, add the following:

```
DJANGO_SETTINGS_MODULE=takeopinion.settings_prod
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=your-render-url.onrender.com
```

### 4. Create a Database (Optional but Recommended)

1. In your Render dashboard, click "New" and select "PostgreSQL"
2. Give it a name (e.g., takeopinion-db)
3. Once created, copy the "Internal Database URL"
4. Add it as an environment variable in your web service:
   ```
   DATABASE_URL=your-internal-database-url
   ```

### 5. Deploy

Click "Create Web Service" and Render will automatically deploy your application.

## Static Files

The application includes static files (CSS, JavaScript, and images) that are automatically collected during the build process. The logo.svg file and other static assets will be served correctly in production.

To verify that static files are being served correctly, visit the `/static-check/` endpoint after deployment.

## Media Files

The application now includes a media directory for user uploads. This directory should be included in your deployment package and must be writable by the application.

## Database

The application includes a SQLite database file (db.sqlite3) which contains all the application data. This file should be included in your deployment package.

## Custom Domain (Optional)

1. In your web service settings, go to "Custom Domains"
2. Add your domain
3. Follow the instructions to configure your DNS

## Environment Variables

The following environment variables can be configured:

- `SECRET_KEY`: Django secret key (required)
- `DEBUG`: Set to False for production (default: False)
- `ALLOWED_HOSTS`: Comma-separated list of allowed hosts
- `DATABASE_URL`: Database connection URL (if using external database)
- `DJANGO_SETTINGS_MODULE`: Django settings module (default: takeopinion.settings_prod)

## Troubleshooting

### Common Issues

1. **Build Failures**: Check the build logs for dependency issues
2. **Application Crashes**: Check the application logs for runtime errors
3. **Database Connection**: Ensure DATABASE_URL is correctly set if using external database
4. **Static Files Not Found**: Check that the build process completed successfully and that STATIC_ROOT is correctly configured
5. **Media Files Not Accessible**: Ensure the media directory is writable

### Useful Commands

To run management commands on Render:

1. Go to your web service dashboard
2. Click "Shell" in the "Manual Deploy" section
3. Run your commands (e.g., `python manage.py migrate`)

## Updating the Application

To update your deployed application:

1. Push changes to your GitHub repository
2. Go to your Render dashboard
3. Click "Manual Deploy" and select "Deploy latest commit"

Or set up auto-deploy to automatically deploy new commits.

## Scaling

Render automatically handles scaling for most applications. For high-traffic applications:

1. Go to your web service settings
2. Adjust the instance type and count as needed
3. Consider adding a CDN for static assets

## Recent Fixes

The following issues have been addressed in the latest deployment setup:

1. **Requirements File**: Cleaned up the requirements.txt file to only include essential packages
2. **Python Version**: Specified Python 3.11 for compatibility with Render
3. **Build Script**: Updated build script with pip upgrade command for better reliability
4. **Static Files**: Verified static files collection and serving
5. **Gunicorn Configuration**: Fixed missing os import and simplified start command
6. **Deployment Command**: Ensured correct start command is used for Render deployment
7. **Settings Configuration**: Fixed ALLOWED_HOSTS configuration and ensured production settings are used correctly
8. **Media Files Support**: Added media file configuration to settings and URL routing
9. **Cache Cleanup**: Removed all __pycache__ directories and .pyc files for cleaner deployment

## Render Deployment Cache Issue

If you're experiencing the error "Error: 'gunicorn.conf.py' doesn't exist" even after our fixes, this is due to Render's build cache retaining the old configuration.

### Solution

1. Go to your Render dashboard
2. Navigate to your web service
3. Click on "Manual Deploy" 
4. Select "Clear build cache & deploy"

This will force Render to rebuild your application from scratch using the updated configuration from your render.yaml file which specifies the correct start command:
`gunicorn --bind 0.0.0.0:$PORT takeopinion.wsgi:application`

After clearing the cache, your deployment should work correctly.

## Common Issues and Solutions

### DisallowedHost Error

If you encounter a "DisallowedHost at /" error, it means the domain is not in the ALLOWED_HOSTS setting. This has been fixed in the latest version by:

1. Ensuring the DJANGO_SETTINGS_MODULE environment variable is properly set to use takeopinion.settings_prod
2. Correctly configuring ALLOWED_HOSTS in settings_prod.py to include .onrender.com
3. Updating wsgi.py and manage.py to default to production settings

To fix this issue:

1. Ensure your render.yaml file includes:
   ```yaml
   - key: DJANGO_SETTINGS_MODULE
     value: takeopinion.settings_prod
   - key: ALLOWED_HOSTS
     value: .onrender.com
   ```
2. Clear Render's build cache and redeploy

## Deployment Checklist

For a complete deployment checklist, refer to the DEPLOYMENT_CHECKLIST.md file which includes:

- All files and directories that should be included
- Pre-deployment tasks completed
- Deployment instructions
- Post-deployment verification steps