from django import template

register = template.Library()

@register.filter
def split(value, separator=' '):
    """Split a string by separator and return the first part"""
    if not value:
        return ''
    parts = value.split(separator)
    return parts[0] if parts else ''