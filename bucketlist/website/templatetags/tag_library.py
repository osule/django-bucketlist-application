# templatetags/tag_library.py

from django import template

register = template.Library()

@register.filter(name="to_str")  # registers the `to_str` filter
def to_str(value):
    """converts any value to a string representation"""
    return str(value)