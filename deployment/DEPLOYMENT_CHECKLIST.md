# TakeOpinion Deployment Checklist

## Pre-Deployment ✅

- [x] Exported all existing data to JSON fixtures
- [x] Verified all data is preserved (4 bookings, 3 doctors, 4 hospitals, 9 treatments, 3 accommodations)
- [x] Created deployment scripts and documentation
- [x] Updated build process to automatically import data
- [x] Committed all changes to GitHub
- [x] Verified repository is clean with no uncommitted changes

## Deployment to Render

### Step 1: Render Dashboard Setup
- [ ] Go to https://render.com/dashboard
- [ ] Click "New" → "Web Service"
- [ ] Connect your GitHub repository
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

### Step 3: Admin Interface
- [ ] Access `/admin` URL
- [ ] Login with superuser credentials
- [ ] Verify all data models are accessible
- [ ] Test creating/editing content

### Step 4: User Features
- [ ] Test user registration/login
- [ ] Verify search functionality
- [ ] Check reviews system
- [ ] Test booking flow end-to-end

## Troubleshooting

### Common Issues

1. **Build Failures**
   - Check build logs in Render dashboard
   - Verify requirements.txt has all dependencies
   - Ensure build.sh has correct permissions

2. **Data Not Imported**
   - Check if fixtures directory exists
   - Verify import_data.py script runs correctly
   - Check build logs for import errors

3. **Static Files Not Loading**
   - Verify WhiteNoise configuration
   - Check if collectstatic ran during build
   - Confirm STATIC_ROOT and STATIC_URL settings

4. **Application Errors**
   - Check application logs in Render
   - Verify environment variables are set
   - Ensure ALLOWED_HOSTS includes your domain

### Manual Data Import (if needed)

If automatic data import fails:

1. SSH into your Render instance
2. Run: `python manage.py loaddata fixtures/*`

## Scaling and Monitoring

### Performance Optimization
- [ ] Consider upgrading to paid plan for production
- [ ] Add PostgreSQL database for better performance
- [ ] Configure Redis for caching
- [ ] Set up CDN for static files

### Monitoring
- [ ] Enable Render monitoring alerts
- [ ] Set up logging aggregation
- [ ] Configure uptime monitoring
- [ ] Set up performance metrics

## Maintenance

### Regular Tasks
- [ ] Monitor application logs
- [ ] Check disk space usage
- [ ] Update dependencies periodically
- [ ] Backup database regularly

### Updates
1. Make changes locally
2. Run export_data.py to update fixtures
3. Commit and push to GitHub
4. Render will auto-deploy (if enabled) or manually trigger deploy

## Support

For deployment issues, contact:
- Render Support: https://render.com/help
- Development team for application-specific issues

---

✅ **Deployment Ready!** All data preserved and application prepared for Render deployment.