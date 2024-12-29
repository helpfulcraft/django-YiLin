from django.contrib import admin
from .models import Banner, Statistics

# Register your models here.

@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ('title', 'order', 'is_active', 'start_time', 'end_time', 'created_time')
    list_filter = ('is_active',)
    search_fields = ('title', 'subtitle', 'description')
    list_editable = ('order', 'is_active')
    date_hierarchy = 'created_time'

@admin.register(Statistics)
class StatisticsAdmin(admin.ModelAdmin):
    list_display = ('title', 'value', 'icon', 'order', 'is_active', 'created_time')
    list_filter = ('is_active',)
    search_fields = ('title',)
    list_editable = ('value', 'order', 'is_active')
