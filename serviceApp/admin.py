from django.contrib import admin
from .models import ServiceCategory, Service, ServiceAppointment, ServiceReview

@admin.register(ServiceCategory)
class ServiceCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'icon', 'index')
    search_fields = ('name',)
    ordering = ('index',)

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'status', 'price', 'duration', 'is_featured', 'created_time')
    list_filter = ('status', 'is_featured', 'category', 'created_time')
    search_fields = ('name', 'short_description', 'content')
    date_hierarchy = 'created_time'
    list_editable = ('status', 'is_featured')
    readonly_fields = ('created_time', 'updated_time')
    fieldsets = (
        ('基本信息', {
            'fields': ('name', 'category', 'image', 'short_description')
        }),
        ('服务详情', {
            'fields': ('content', 'price', 'duration')
        }),
        ('状态', {
            'fields': ('status', 'is_featured')
        }),
        ('时间信息', {
            'fields': ('created_time', 'updated_time'),
            'classes': ('collapse',)
        }),
    )

@admin.register(ServiceAppointment)
class ServiceAppointmentAdmin(admin.ModelAdmin):
    list_display = ('service', 'user', 'appointment_time', 'status', 'created_time')
    list_filter = ('status', 'appointment_time', 'created_time')
    search_fields = ('service__name', 'user__username', 'note')
    date_hierarchy = 'appointment_time'
    list_editable = ('status',)
    readonly_fields = ('created_time', 'updated_time')

@admin.register(ServiceReview)
class ServiceReviewAdmin(admin.ModelAdmin):
    list_display = ('service', 'user', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('service__name', 'user__username', 'content')
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at',)
