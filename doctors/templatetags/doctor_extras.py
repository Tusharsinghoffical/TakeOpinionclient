from django import template
import re

register = template.Library()

@register.filter
def split(value, separator=' '):
    """Split a string by separator and return the first part"""
    if not value:
        return ''
    parts = value.split(separator)
    return parts[0] if parts else ''

@register.filter
def youtube_video_id(url):
    """Extract YouTube video ID from URL"""
    if not url:
        return ''
    
    # Pattern for YouTube URLs
    patterns = [
        r'youtube\.com/watch\?v=([^&]+)',
        r'youtu\.be/([^?]+)',
        r'youtube\.com/embed/([^?]+)'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    
    return ''

@register.filter
def vimeo_video_id(url):
    """Extract Vimeo video ID from URL"""
    if not url:
        return ''
    
    # Pattern for Vimeo URLs
    pattern = r'vimeo\.com/(\d+)'
    match = re.search(pattern, url)
    if match:
        return match.group(1)
    
    return ''