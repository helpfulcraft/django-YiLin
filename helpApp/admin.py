from django.contrib import admin
from .models import HelpCategory, HelpArticle, FAQ, Guide, Feedback, OnlineConsultation

# Register your models here.

@admin.register(HelpCategory)
class HelpCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'order', 'created_time')
    list_filter = ('created_time',)
    search_fields = ('name', 'description')
    ordering = ('order', 'created_time')

@admin.register(HelpArticle)
class HelpArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'views', 'is_published', 'created_time')
    list_filter = ('category', 'is_published', 'created_time')
    search_fields = ('title', 'content')
    ordering = ('-created_time',)

@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('question', 'category', 'order', 'is_published', 'created_time')
    list_filter = ('category', 'is_published', 'created_time')
    search_fields = ('question', 'answer')
    ordering = ('order', '-created_time')

@admin.register(Guide)
class GuideAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'order', 'is_published', 'created_time')
    list_filter = ('category', 'is_published', 'created_time')
    search_fields = ('title', 'content')
    ordering = ('order', '-created_time')

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'status', 'created_time')
    list_filter = ('status', 'created_time')
    search_fields = ('title', 'content', 'user__username')
    ordering = ('-created_time',)

@admin.register(OnlineConsultation)
class OnlineConsultationAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'category', 'status', 'created_time')
    list_filter = ('category', 'status', 'created_time')
    search_fields = ('title', 'content', 'user__username')
    ordering = ('-created_time',)
