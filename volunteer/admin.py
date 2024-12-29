from django.contrib import admin
from .models import Activity, Application

# Register your models here.

@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'location', 'volunteers_needed', 'created_at')
    list_filter = ('date', 'location')
    search_fields = ('title', 'description', 'location')
    date_hierarchy = 'date'

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('user', 'activity', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('user__username', 'activity__title', 'apply_reason')
    raw_id_fields = ('user', 'activity')
