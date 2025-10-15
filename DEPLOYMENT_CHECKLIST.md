# TakeOpinion Deployment Checklist

## Pre-Deployment ✅

- [x] Exported all existing data to JSON fixtures
- [x] Verified all data is preserved (4 bookings, 3 doctors, 4 hospitals, 9 treatments, 3 accommodations)
- [x] Created deployment scripts and documentation
- [x] Updated build process to automatically import data
- [x] Verified repository is clean with no uncommitted changes

## Deployment to Render

### Step 1: Render Dashboard Setup
- [ ] Go to https://render.com/dashboard
- [ ] Click "New" → "Web Service"
- [ ] Configure your deployment package
- [ ] Select branch: main

### Step 2: Service Configuration
- [ ] **Name**: takeopinion (or your preferred name)
- [ ] **Environment**: Python
- [ ] **Build Command**: `./build.sh`
- [ ] **Start Command**: `gunicorn --bind 0.0.0.0:$PORT takeopinion.wsgi:application`
- [ ] **Plan**: Free or paid (your choice)

### Step 3: Environment Variables
- [ ] `DJANGO_SETTINGS_MODULE` = `takeopinion.settings_prod`
- [ ] `SECRET_KEY` = (auto-generated or your own)
- [ ] `DEBUG` = `False`
- [ ] `ALLOWED_HOSTS` = `.onrender.com,your-app-name.onrender.com`

### Step 4: Advanced Settings (Optional)
- [ ] Auto-deploy: Yes
- [ ] Health Check Path: `/`

### Step 5: Deploy
- [ ] Click "Create Web Service"
- [ ] Wait for build and deployment to complete (~5-10 minutes)

## Post-Deployment Verification

### Step 1: Basic Functionality
- [ ] Visit your Render URL
- [ ] Verify homepage loads correctly
- [ ] Check navigation works
- [ ] Verify all links function properly

### Step 2: Data Verification
- [ ] Check that all doctors are present
- [ ] Verify all hospitals are listed
- [ ] Confirm treatments are displayed
- [ ] Test booking functionality
- [ ] Verify hotel recommendations appear

### Step 3: Administrative Tasks
- [ ] Create superuser account
- [ ] Verify admin dashboard access
- [ ] Test content management features
- [ ] Verify user registration and login

## Maintenance

### Regular Tasks
- [ ] Monitor application logs
- [ ] Check disk space usage
- [ ] Verify SSL certificate validity
- [ ] Backup database regularly

### Updates
1. Make changes locally
2. Run export_data.py to update fixtures
3. Update your deployment package
4. Manually trigger deploy

## Support

For deployment issues, contact: