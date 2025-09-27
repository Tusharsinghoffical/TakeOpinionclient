# Render Deployment Guide for TakeOpinion

This guide explains how to deploy the TakeOpinion Django application on Render.

## Prerequisites

1. A Render account (https://render.com)
2. This repository connected to your Render account

## Deployment Steps

### 1. Create a New Web Service on Render

1. Go to your Render Dashboard
2. Click "New" and select "Web Service"
3. Connect your repository (GitHub, GitLab, etc.)
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

To access the Django admin:

1. Open a shell in the Render dashboard
2. Run: `python manage.py createsuperuser`
3. Follow the prompts to create an admin user

### 3. Collect Static Files

The build script already runs this, but if needed:

1. Open a shell in the Render dashboard
2. Run: `python manage.py collectstatic --noinput`

## Database Considerations

The application is currently configured to use SQLite, which is not recommended for production on Render. For a production database:

1. Provision a PostgreSQL database on Render
2. Update your environment variables to include:
   ```
   DATABASE_URL=your-postgresql-connection-url
   ```

The application is already configured to use `dj_database_url` to parse the DATABASE_URL environment variable.

## Custom Domain (Optional)

To use a custom domain:

1. In your Render service settings, go to "Custom Domains"
2. Add your domain
3. Follow the instructions to configure DNS records with your domain provider

## Environment Variables Reference

| Variable | Description | Required |
|----------|-------------|----------|
| `DJANGO_SETTINGS_MODULE` | Django settings module | Yes |
| `SECRET_KEY` | Django secret key | Yes |
| `DEBUG` | Django debug mode | Yes |
| `ALLOWED_HOSTS` | Comma-separated list of allowed hosts | Yes |
| `DATABASE_URL` | Database connection URL (optional for SQLite) | No |

## Troubleshooting

### Common Issues

1. **Application fails to start**: Check the logs in the Render dashboard
2. **Static files not loading**: Ensure `collectstatic` ran during build
3. **Database errors**: Verify database configuration and run migrations
4. **Permission errors**: Check file permissions in your repository

### Checking Logs

1. Go to your service dashboard on Render
2. Click "Logs" to view real-time application logs

## Updating the Application

To update your deployed application:

1. Push changes to your repository
2. Render will automatically deploy if auto-deploy is enabled
3. Or manually trigger a deploy from the Render dashboard

## Support

For issues with this deployment configuration, please check:
- Render's documentation: https://render.com/docs
- Django's deployment documentation: https://docs.djangoproject.com/en/5.2/howto/deployment/