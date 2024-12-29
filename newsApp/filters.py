import django_filters
from django.db.models import Q
from .models import News

class NewsFilter(django_filters.FilterSet):
    """新闻过滤器"""
    q = django_filters.CharFilter(method='filter_search', label='搜索')
    category = django_filters.NumberFilter(field_name='category', label='分类')
    tag = django_filters.NumberFilter(field_name='tags', label='标签')
    
    class Meta:
        model = News
        fields = ['q', 'category', 'tag']
    
    def filter_search(self, queryset, name, value):
        """搜索过滤"""
        return queryset.filter(
            Q(title__icontains=value) |
            Q(summary__icontains=value) |
            Q(content__icontains=value)
        )
