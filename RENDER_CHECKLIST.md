# Render Deployment Checklist

## Pre-deployment Checklist

### Repository Configuration
- [ ] All code changes are committed and pushed to GitHub
- [ ] [.gitignore](file:///c%3A/Users/tusha/Desktop/Client%202/.gitignore) file is properly configured
- [ ] No compiled Python files (.pyc) are tracked

### Render Configuration Files
- [ ] [render.yaml](file:///c%3A/Users/tusha/Desktop/Client%202/render.yaml) exists and is correctly configured
- [ ] [build.sh](file:///c%3A/Users/tusha/Desktop/Client%202/build.sh) exists and has proper permissions
- [ ] [runtime.txt](file:///c%3A/Users/tusha/Desktop/Client%202/runtime.txt) specifies Python 3.11
- [ ] [requirements.txt](file:///c%3A/Users/tusha/Desktop/Client%202/requirements.txt) includes all dependencies

### Django Configuration
- [ ] [settings_prod.py](file:///c%3A/Users/tusha/Desktop/Client%202/takeopinion/settings_prod.py) properly configured
- [ ] [wsgi.py](file:///c%3A/Users/tusha/Desktop/Client%202/takeopinion/wsgi.py) defaults to production settings
- [ ] [ALLOWED_HOSTS](file://c:\Users\tusha\Desktop\Client%202\takeopinion\settings_prod.py#L18-L18) includes .onrender.com
- [ ] DEBUG is set to False in production settings
- [ ] WhiteNoise is configured for static files serving

### Static Files
- [ ] Static files directory structure is correct
- [ ] [logo.svg](file:///c%3A/Users/tusha/Desktop/Client%202/static/images/logo.svg) and other assets exist
- [ ] Static files collection is working in build script
- [ ] WhiteNoise middleware is added for static file serving

## Deployment Steps

### Initial Deployment
1. Go to Render Dashboard
2. Create new Web Service
3. Connect to your GitHub repository
4. Ensure correct settings:
   - Build Command: `./build.sh`
   - Start Command: `gunicorn --bind 0.0.0.0:$PORT takeopinion.wsgi:application`

### Clear Cache Deployment (If Previous Deployments Failed)
1. Go to your Render dashboard
2. Navigate to your web service
3. Click on "Manual Deploy"
4. Select "Clear build cache & deploy"

## Common Issues and Solutions

### 1. DisallowedHost Error
**Solution**:
1. Ensure [render.yaml](file:///c%3A/Users/tusha/Desktop/Client%202/render.yaml) has:
   ```yaml
   - key: ALLOWED_HOSTS
     value: .onrender.com
   ```
2. Clear Render build cache and redeploy

### 2. Static Files Not Loading
**Solution**:
1. Ensure [build.sh](file:///c%3A/Users/tusha/Desktop/Client%202/build.sh) includes:
   ```bash
   python manage.py collectstatic --noinput
   ```
2. Ensure WhiteNoise is added to [requirements.txt](file:///c%3A/Users/tusha/Desktop/Client%202/requirements.txt) and configured in settings
3. Clear Render build cache and redeploy

### 3. Database Migration Issues
**Solution**:
1. Ensure [build.sh](file:///c%3A/Users/tusha/Desktop/Client%202/build.sh) includes:
   ```bash
   python manage.py migrate
   ```

## Additional Notes

### Static Files on Render
Render requires special handling for static files. We've configured WhiteNoise to serve static files directly from Django, which is the recommended approach for Django applications on Render.

### Debugging Static Files Issues
If static files are still not loading:
1. Check the Render logs for any errors during the build process
2. Verify that the collectstatic command ran successfully
3. Ensure WhiteNoise is properly configured in middleware
4. Check that static files exist in the static directory