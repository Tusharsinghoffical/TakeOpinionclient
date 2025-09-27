# Deployment to Render

This document explains how to deploy the TakeOpinion application to Render with all data preserved.

## Prerequisites

1. A Render account (https://render.com)
2. A GitHub account with this repository
3. Python 3.11+ installed locally

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
3. Connect your GitHub repository
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
- Fixtures are committed to the repository
- During deployment, data is automatically imported from fixtures

### 5. Post-Deployment

After deployment:
1. Visit your Render URL
2. Verify all data is present
3. Test booking functionality
4. Test hotel recommendations

## Troubleshooting

### Common Issues

1. **Build failures**: Check the build logs in Render dashboard
2. **Data not imported**: Ensure fixtures directory exists and contains data
3. **Static files not loading**: Check WhiteNoise configuration
4. **Database errors**: Verify database migrations run correctly

### Manual Data Import

If automatic import fails:

```bash
# SSH into your Render instance
# Run:
python manage.py loaddata fixtures/*
```

## Environment Variables

Required environment variables:
- `DJANGO_SETTINGS_MODULE`: takeopinion.settings_prod
- `SECRET_KEY`: Your Django secret key
- `DEBUG`: False
- `ALLOWED_HOSTS`: Your Render domain(s)

## Scaling

Render automatically scales your application based on traffic. For high-traffic applications:
1. Consider upgrading to a paid plan
2. Add a PostgreSQL database
3. Configure Redis for caching

## Monitoring

Render provides built-in monitoring:
- Logs accessible from dashboard
- Automatic restart on failures
- Performance metrics