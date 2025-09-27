# Doctor Management Guide

This guide explains how to manage doctor information through the Django admin panel.

## Accessing the Admin Panel

1. Start your Django development server:
   ```
   python manage.py runserver
   ```

2. Navigate to: http://127.0.0.1:8000/admin/

3. Log in with your admin credentials

## Managing Doctor Information

### 1. Adding a New Doctor

1. In the admin panel, click on "Doctors" under the "Doctors" section
2. Click the "ADD DOCTOR" button
3. Fill in all the required information:
   - **Name**: Doctor's full name
   - **Slug**: URL-friendly version of the name (auto-generated)
   - **Specialization**: Medical specialization (e.g., Cardiologist, Orthopedic Surgeon)
   - **About**: Detailed biography of the doctor
   - **Key Points**: Brief highlights of the doctor's expertise
   - **Education**: Educational qualifications
   - **Experience Years**: Number of years of experience
   - **Contact Information**: Phone, Email, Website
   - **Rating**: Doctor's rating (0.0 to 5.0)
   - **Review Count**: Number of patient reviews
   - **Professional Details**: Medical license number, Languages spoken
   - **Affiliations**: Select associated hospitals and treatments

### 2. Managing Doctor Media (Images/Videos)

1. When editing a doctor, scroll down to the "Doctor media" section
2. Click "Add another Doctor media" to add new media items
3. For each media item:
   - Enter an **Image URL** (direct link to an image)
   - Or enter a **Video URL** (YouTube, Vimeo, etc.)
4. Save the doctor to apply changes

### 3. Associating Hospitals and Treatments

1. In the doctor editing form, scroll to the "Affiliations" section
2. **Hospitals**: Select hospitals where the doctor practices
3. **Treatments**: Select treatments that the doctor specializes in

## Best Practices

### For Images:
- Use high-quality images with a 1:1 aspect ratio (square) for profile pictures
- Use 16:9 aspect ratio for gallery images
- Ensure images are publicly accessible via direct URLs
- Good sources: Unsplash, Pexels, or your own image hosting

### For Data Entry:
- Keep key points concise but informative (3-5 key points)
- Use consistent formatting for educational qualifications
- Regularly update ratings and review counts
- Verify all URLs are working correctly

## Example Data

### Sample Doctor Media URLs:
- **Profile Image**: `https://ui-avatars.com/api/?name=Dr.+Arjun+Mehta&background=0D6EFD&color=fff&size=256`
- **Gallery Image**: `https://images.unsplash.com/photo-1519494026892-80bbd2d6fd0d?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1200&q=80`

### Sample Contact Information:
- **Phone**: +91 98765 43210
- **Email**: doctor@hospitalname.com
- **Website**: https://www.hospitalname.com/doctors/doctor-name

## Troubleshooting

### If images are not displaying:
1. Check that the image URLs are direct links to image files
2. Verify that the URLs are publicly accessible
3. Ensure the URLs start with https://

### If information is not updating on the website:
1. Make sure you clicked "Save" after making changes
2. Clear your browser cache
3. Check that you're viewing the correct doctor page

## Need Help?

For technical support, contact the development team.