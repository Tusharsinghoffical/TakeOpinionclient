import os
import sys
import django

# Add the project directory to the Python path
sys.path.append("c:\\Users\\tusha\\Desktop\\Client 2")

# Set the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'takeopinion.settings')

# Setup Django
django.setup()

from hospitals.models import HospitalMedia

def update_hospital_media():
    # Get all hospital media items
    media_items = HospitalMedia.objects.all()
    print(f"Found {media_items.count()} media items")
    
    # Update with valid Unsplash URLs
    unsplash_urls = [
        "https://images.unsplash.com/photo-1519494026892-80bbd2d6fd0d?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1200&q=80",
        "https://images.unsplash.com/photo-1532938911079-1b06ac7ceec7?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1200&q=80",
        "https://images.unsplash.com/photo-1512678080530-7760d21f6c84?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1200&q=80",
        "https://images.unsplash.com/photo-1519521397967-61a5640c7145?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1200&q=80",
        "https://images.unsplash.com/photo-1516738901171-8eb4fc13bd20?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1200&q=80"
    ]
    
    for i, media in enumerate(media_items):
        # Check if the URL is invalid (Google Drive links or example.com)
        if "example.com" in media.image_url or "drive.google.com" in media.image_url or not media.image_url:
            media.image_url = unsplash_urls[i % len(unsplash_urls)]
            media.save()
            print(f"Updated media item {media.id} with URL: {media.image_url}")
        else:
            print(f"Media item {media.id} already has valid URL: {media.image_url}")

if __name__ == "__main__":
    update_hospital_media()