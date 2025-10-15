# Render Deployment Guide for TakeOpinion

This guide explains how to deploy the TakeOpinion Django application on Render.

## Prerequisites

1. A Render account (https://render.com)
2. This repository prepared for deployment

## Deployment Steps

### 1. Create a New Web Service on Render

1. Go to your Render Dashboard
2. Click "New" and select "Web Service"
3. Configure your deployment package
4. Select the branch you want to deploy (usually `main` or `master`)

### 2. Configure the Web Service

Render will automatically detect this is a Python application. Confirm the following settings:

- **Name**: takeopinion (or any name you prefer)
- **Environment**: Python
- **Build Command**: `./build.sh`
- **Start Command**: `gunicorn --bind 0.0.0.0:$PORT takeopinion.wsgi:application`
- **Auto-Deploy**: Yes (recommended)

### 3. Environment Variables

Set the following environment variables in the Render dashboard:

```
DJANGO_SETTINGS_MODULE=takeopinion.settings_prod
SECRET_KEY=your-secret-key-here (generate a secure one)
DEBUG=False
ALLOWED_HOSTS=takeopinionclient.onrender.com,.onrender.com
```

Note: Render can automatically generate a SECRET_KEY for you if you prefer.

### 4. Advanced Settings

- **Instance Type**: Free or Standard (based on your needs)
- **Disk**: Add a persistent disk if you're using SQLite (not recommended for production)

### 5. Deploy

Click "Create Web Service" to start the deployment process.

## Post-Deployment Steps

### 1. Run Initial Migrations

After the first deployment, you'll need to run migrations:

1. Go to your service dashboard on Render
2. Click "Shell" to open a terminal
3. Run: `python manage.py migrate`

### 2. Create a Superuser (Optional)

To access the admin dashboard:

1. Open a shell in the Render dashboard
2. Run: `python manage.py createsuperuser`
3. Follow the prompts to create an admin account

### 3. Verify Deployment

1. Visit your deployed application URL
2. Test key functionality (search, booking, etc.)
3. Log in to the admin dashboard
4. Verify all data is present

## Updating the Application

To update your deployed application:

1. Update your deployment package
2. Go to your Render dashboard
3. Click "Manual Deploy" and select "Deploy latest commit"

Or set up auto-deploy to automatically deploy new commits.

## Troubleshooting

### Common Issues

1. **DisallowedHost Error**: Ensure ALLOWED_HOSTS includes your Render domain
2. **Static Files Not Loading**: Check that the build process completed successfully
3. **Database Connection Issues**: Verify DATABASE_URL environment variable if using external database
4. **Import Errors**: Check that all dependencies are listed in requirements.txt

### Checking Logs

To troubleshoot issues:

1. Go to your service dashboard on Render
2. Click "Logs" to view application logs
3. Check for error messages
4. Look at build logs if deployment fails

## Support

For additional help with deployment, consult the main deployment documentation or Render's support resources.