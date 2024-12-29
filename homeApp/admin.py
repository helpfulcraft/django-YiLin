from django.contrib import admin
from .models import Carousel, Activity, ServiceHighlight, Statistic

# Register your models here.

@admin.register(Carousel)
class CarouselAdmin(admin.ModelAdmin):
    """轮播图管理"""
    list_display = ('title', 'order', 'is_active', 'created_time')
    list_filter = ('is_active',)
    search_fields = ('title', 'description')
    ordering = ('order', '-created_time')

@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    """活动管理"""
    list_display = ('title', 'start_time', 'end_time', 'location', 'volunteers_needed')
    list_filter = ('start_time', 'end_time')
    search_fields = ('title', 'description', 'content')
    ordering = ('-start_time',)

@admin.register(ServiceHighlight)
class ServiceHighlightAdmin(admin.ModelAdmin):
    """服务亮点管理"""
    list_display = ('title', 'icon', 'index', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('title', 'description')
    ordering = ('index',)

@admin.register(Statistic)
class StatisticAdmin(admin.ModelAdmin):
    """统计数据管理"""
    list_display = ('title', 'value', 'icon', 'index', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('title',)
    ordering = ('index',)
