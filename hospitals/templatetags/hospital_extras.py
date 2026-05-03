from django import template
from hotels.models import Hotel

register = template.Library()

@register.simple_tag
def get_nearby_hotels_for_hospital(hospital_id, limit=3):
    """
    Get nearby hotels for a hospital by hospital ID
    """
    try:
        hotels = Hotel._default_manager.filter(nearby_hospitals__id=hospital_id, is_active=True).order_by('-rating')[:limit]
        return hotels
    except:
        return Hotel._default_manager.none()