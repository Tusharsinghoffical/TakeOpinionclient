# Doctor Profile Picture Management

## How to Add Profile Pictures to Doctors

1. **Access Django Admin Panel**
   - Go to http://127.0.0.1:8000/admin/
   - Log in with your admin credentials

2. **Navigate to Doctors**
   - Click on "Doctors" in the admin panel

3. **Edit a Doctor**
   - Click on the doctor you want to add a profile picture to

4. **Add Profile Picture**
   - In the "Basic Information" section, find the "Profile picture" field
   - Enter a valid URL to an image (see examples below)
   - Click "Save"

## Image URL Sources

You can use images from these sources:

1. **Unsplash** (Free high-quality images)
   - Example: https://images.unsplash.com/photo-1612349317150-e413f6a5b16d?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80

2. **Pexels** (Free stock photos)
   - Example: https://images.pexels.com/photos/5325674/pexels-photo-5325674.jpeg?auto=compress&cs=tinysrgb&w=500

3. **UI Avatars** (Generated avatars)
   - Format: https://ui-avatars.com/api/?name=Doctor+Name&background=0D6EFD&color=fff&size=256

## Troubleshooting

If images still don't appear:

1. Check that the URL is valid by opening it in a new browser tab
2. Make sure the URL starts with http:// or https://
3. Ensure the image URL is not broken
4. Clear your browser cache

## Fallback Behavior

If no profile picture is set, the system automatically generates an avatar using UI Avatars service based on the doctor's name.