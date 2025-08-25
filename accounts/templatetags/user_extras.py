from django import template

register = template.Library()

@register.filter
def first_name(value):
    """Return the first word from a full name string"""
    if not value:
        return ""
    return value.split(" ")[0]