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
   - Start Command: `gunicorn -c gunicorn.conf.py takeopinion.wsgi:application`
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