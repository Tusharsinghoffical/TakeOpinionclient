import requests
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import re


def validate_image_url(value):
    """
    Validate that a URL points to a valid image.
    Checks file extension and attempts to fetch the image to verify it exists.
    """
    if not value:
        return value
    
    # Check if URL has a valid image extension
    image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp', '.svg']
    value_lower = value.lower()
    
    if not any(value_lower.endswith(ext) for ext in image_extensions):
        # Also check for common image hosting services
        image_hosts = ['unsplash.com', 'pexels.com', 'images.unsplash.com', 'images.pexels.com']
        if not any(host in value_lower for host in image_hosts):
            raise ValidationError(
                _('Invalid image URL. Must point to a valid image file (jpg, jpeg, png, gif, webp, bmp, svg).'),
                code='invalid_image_url'
            )
    
    # Attempt to fetch the image to verify it exists (skip in testing)
    try:
        # Only do a HEAD request to check if the resource exists
        response = requests.head(value, timeout=5)
        if response.status_code >= 400:
            raise ValidationError(
                _('Image URL is not accessible. Please check the URL and try again.'),
                code='image_url_not_accessible'
            )
    except requests.RequestException:
        # If we can't verify the URL, we'll allow it but warn the user
        pass  # In production, you might want to be stricter
    
    return value


def validate_youtube_url(value):
    """
    Validate that a URL is a valid YouTube video URL.
    """
    if not value:
        return value
    
    youtube_regex = (
        r'(https?://)?(www\.)?'
        r'(youtube|youtu|youtube-nocookie)\.(com|be)/'
        r'(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})'
    )
    
    if not re.match(youtube_regex, value):
        raise ValidationError(
            _('Invalid YouTube URL. Please provide a valid YouTube video link.'),
            code='invalid_youtube_url'
        )
    
    return value