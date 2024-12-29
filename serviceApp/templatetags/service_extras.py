from django import template

register = template.Library()

@register.filter
def get_range(value):
    """
    Creates a range from 0 to the given value.
    Used for rendering star ratings.
    """
    try:
        value = int(value)
        return range(value)
    except (ValueError, TypeError):
        return range(0)
