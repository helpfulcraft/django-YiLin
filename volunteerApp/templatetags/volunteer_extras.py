from django import template

register = template.Library()

@register.filter
def status_color(status):
    """根据活动状态返回对应的Bootstrap颜色类"""
    color_map = {
        'draft': 'secondary',
        'published': 'success',
        'cancelled': 'danger',
        'completed': 'info',
        'pending': 'warning'
    }
    return color_map.get(status, 'secondary')
