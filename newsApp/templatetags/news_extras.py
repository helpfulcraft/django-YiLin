from django import template

register = template.Library()

@register.filter
def remainder(value, arg):
    """
    返回除法的余数
    """
    return value % arg

@register.filter
def subtract(value, arg):
    """
    返回两个数的差
    """
    return value - arg

@register.filter
def get_range(value):
    """
    返回一个范围列表
    """
    return range(value)
