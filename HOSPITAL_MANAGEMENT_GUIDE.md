# Hospital Management Guide

This guide explains how to manage hospital information through the Django admin panel.

## Accessing the Admin Panel

1. Start your Django development server:
   ```
   python manage.py runserver
   ```

2. Navigate to: http://127.0.0.1:8000/admin/

3. Log in with your admin credentials

## Managing Hospital Information

### 1. Adding a New Hospital

1. In the admin panel, click on "Hospitals" under the "Hospitals" section
2. Click the "ADD HOSPITAL" button
3. Fill in all the required information:
   - **Name**: Hospital name
   - **Slug**: URL-friendly version of the name (auto-generated)
   - **Location details**: Country, State, City, Address
   - **Contact information**: Phone, Email, Website
   - **Hospital details**: Established year, Beds count, Staff count, etc.
   - **Certifications**: Check the appropriate boxes for JCI, NABH, ISO certifications
   - **Treatments**: Select from the available treatments (add new treatments if needed)

### 2. Managing Hospital Media (Images/Videos)

1. When editing a hospital, scroll down to the "Hospital media" section
2. Click "Add another Hospital media" to add new media items
3. For each media item:
   - Enter an **Image URL** (direct link to an image)
   - Or enter a **Video URL** (YouTube, Vimeo, etc.)
4. Save the hospital to apply changes

### 3. Adding Treatments

1. In the admin panel, click on "Treatments" under the "Treatments" section
2. Click the "ADD TREATMENT" button
3. Fill in the treatment details:
   - **Name**: Treatment name
   - **Category**: Select from Medical Treatments, Aesthetic, or Wellness
   - **Description**: Detailed description of the treatment
   - **Additional details**: Duration, anesthesia type, recovery time, etc.

### 4. Managing Treatment Categories

1. In the admin panel, click on "Treatment categories" under the "Treatments" section
2. Add new categories or edit existing ones as needed

## Best Practices

### For Images:
- Use high-quality images with a 16:9 aspect ratio (1200x675 pixels or similar)
- Ensure images are publicly accessible via direct URLs
- Good sources: Unsplash, Pexels, or your own image hosting

### For Data Entry:
- Keep descriptions concise but informative
- Use consistent formatting for contact information
- Regularly update ratings and review counts
- Verify all URLs are working correctly

## Example Data

### Sample Hospital Media URLs:
- **Unsplash**: `https://images.unsplash.com/photo-1519494026892-80bbd2d6fd0d?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1200&q=80`
- **Picsum**: `https://picsum.photos/1200/675?random=1`

### Sample Contact Information:
- **Phone**: +91 11 2345 6789
- **Email**: info@hospitalname.com
- **Website**: https://www.hospitalname.com

## Troubleshooting

### If images are not displaying:
1. Check that the image URLs are direct links to image files
2. Verify that the URLs are publicly accessible
3. Ensure the URLs start with https://

### If information is not updating on the website:
1. Make sure you clicked "Save" after making changes
2. Clear your browser cache
3. Check that you're viewing the correct hospital page

## Need Help?

For technical support, contact the development team.