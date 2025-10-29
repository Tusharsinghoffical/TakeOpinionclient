from django import template
from ..models import Hotel

register = template.Library()

@register.simple_tag
def get_nearby_hotels(hospital, limit=3):
    """
    Get nearby hotels for a hospital
    """
    if hospital:
        return Hotel._default_manager.filter(nearby_hospitals=hospital, is_active=True).order_by('-rating')[:limit]
    return Hotel._default_manager.none()