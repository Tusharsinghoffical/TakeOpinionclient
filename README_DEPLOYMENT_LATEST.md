# TakeOpinion Deployment Instructions

This document provides instructions for deploying the TakeOpinion application to Render.

## Prerequisites

- A Render account
- This repository connected to Render
- All dependencies listed in [requirements.txt](file:///c%3A/Users/tusha/Desktop/Client%202/requirements.txt)

## Deployment Files

The following files are essential for deployment:

1. **[render.yaml](file:///c%3A/Users/tusha/Desktop/Client%202/render.yaml)** - Main Render configuration
2. **[build.sh](file:///c%3A/Users/tusha/Desktop/Client%202/build.sh)** - Build script executed during deployment
3. **[requirements.txt](file:///c%3A/Users/tusha/Desktop/Client%202/requirements.txt)** - Python dependencies
4. **[runtime.txt](file:///c%3A/Users/tusha/Desktop/Client%202/runtime.txt)** - Python version specification
5. **[manage.py](file:///c%3A/Users/tusha/Desktop/Client%202/manage.py)** - Django management script

## Deployment Process

1. Ensure all files are properly formatted with Unix line endings (LF)
2. Push changes to your repository:
   ```bash
   git add .
   git commit -m "Update deployment configuration"
   git push origin main
   ```
3. Render will automatically detect the [render.yaml](file:///c%3A/Users/tusha/Desktop/Client%202/render.yaml) file and start the deployment

## Configuration

The application is configured to:
- Use Python 3.11 (specified in [runtime.txt](file:///c%3A/Users/tusha/Desktop/Client%202/runtime.txt))
- Run migrations automatically during build
- Collect static files during build
- Use production settings ([takeopinion.settings_prod](file:///c%3A/Users/tusha/Desktop/Client%202/takeopinion/settings_prod.py))
- Serve the application using Gunicorn

## Environment Variables

Render automatically sets the following environment variables:
- `PORT` - The port the application should listen on
- `SECRET_KEY` - Generated automatically by Render
- `DEBUG` - Set to "False" for production

Additional environment variables can be configured in the Render dashboard.