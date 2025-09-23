# Scripts Directory

This directory contains all the batch files and scripts for managing the TakeOpinion application.

## Batch Files

1. **start_app.bat** - Starts the development server
2. **db_manage.bat** - Database management tool with options for migrations, superuser creation, and database reset
3. **deploy.bat** - Deploys the application to Render (original deployment script)
4. **deploy_mongodb.bat** - Deploys the application to Render with MongoDB support

## Other Scripts

1. **build.sh** - Build script for Render deployment
2. **run_production.py** - Production server runner
3. **render.yaml** - Render deployment configuration

## Usage

To use any of these scripts, navigate to this directory and run the desired batch file:

```cmd
cd scripts
start_app.bat
```

Note: All scripts are designed to work from this directory and will automatically navigate to the parent directory as needed.