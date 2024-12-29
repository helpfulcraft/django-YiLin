from django.contrib import admin
from .models import ActivityCategory, VolunteerActivity, VolunteerApplication, VolunteerProfile

@admin.register(ActivityCategory)
class ActivityCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'order')
    search_fields = ('name', 'description')
    ordering = ('order', 'name')

@admin.register(VolunteerActivity)
class VolunteerActivityAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'location', 'start_time', 'end_time', 
                   'required_volunteers', 'current_volunteers', 'status', 'organizer')
    list_filter = ('status', 'category', 'start_time', 'created_time')
    search_fields = ('title', 'description', 'location')
    date_hierarchy = 'start_time'
    list_editable = ('status',)
    readonly_fields = ('created_time', 'updated_time', 'current_volunteers')
    fieldsets = (
        ('基本信息', {
            'fields': ('title', 'description', 'category', 'image')
        }),
        ('活动详情', {
            'fields': ('location', 'start_time', 'end_time', 'required_volunteers', 'current_volunteers')
        }),
        ('状态信息', {
            'fields': ('status', 'organizer', 'created_time', 'updated_time')
        }),
    )
    raw_id_fields = ('organizer',)

@admin.register(VolunteerApplication)
class VolunteerApplicationAdmin(admin.ModelAdmin):
    list_display = ('user', 'activity', 'status', 'created_time')
    list_filter = ('status', 'created_time')
    search_fields = ('user__username', 'activity__title', 'message')
    date_hierarchy = 'created_time'
    list_editable = ('status',)
    readonly_fields = ('created_time', 'updated_time')
    raw_id_fields = ('user', 'activity')

    def save_model(self, request, obj, form, change):
        if not change:  # 如果是新建申请
            # 检查是否已经存在相同用户对同一活动的申请
            existing = VolunteerApplication.objects.filter(
                user=obj.user,
                activity=obj.activity
            ).exists()
            if existing:
                from django.core.exceptions import ValidationError
                raise ValidationError('该用户已经申请过这个活动了')
        
        # 如果状态改变为已通过，更新活动的志愿者数量
        if change and obj.status == 'approved' and form.initial['status'] != 'approved':
            obj.activity.current_volunteers += 1
            obj.activity.save()
        elif change and form.initial['status'] == 'approved' and obj.status != 'approved':
            obj.activity.current_volunteers -= 1
            obj.activity.save()
        
        super().save_model(request, obj, form, change)

@admin.register(VolunteerProfile)
class VolunteerProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'total_hours', 'skill_tags', 'created_time')
    search_fields = ('user__username', 'skill_tags', 'introduction')
    list_filter = ('created_time',)
    readonly_fields = ('created_time', 'updated_time')
    raw_id_fields = ('user',)
