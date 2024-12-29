from django import template

register = template.Library()

@register.filter
def class_name(obj):
    """返回对象的类名"""
    return obj.__class__.__name__
