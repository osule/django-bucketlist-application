# templatetags/tag_library.py

from django import template

register = template.Library()

@register.filter(name="to_str")
def to_str(value):
    return str(value)