# courses/templatetags/course_tags.py

from django import template
import os

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """Get item from dictionary using key"""
    return dictionary.get(key, {})

@register.filter
def duration_format(minutes):
    """Format duration in hours and minutes"""
    if minutes < 60:
        return f"{minutes} min"
    hours = minutes // 60
    mins = minutes % 60
    if mins == 0:
        return f"{hours}h"
    return f"{hours}h {mins}m"

@register.filter
def basename(value):
    """Get basename of a file path"""
    if not value:
        return ""
    name = value.name if hasattr(value, 'name') else str(value)
    return os.path.basename(name)