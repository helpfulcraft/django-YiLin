from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from .models import NewsCategory, News, NewsComment

@admin.register(NewsCategory)
class NewsCategoryAdmin(admin.ModelAdmin):
    """新闻分类管理"""
    list_display = ('name', 'description', 'news_count', 'created_time')
    search_fields = ('name', 'description')
    list_filter = ('created_time',)
    
    def news_count(self, obj):
        """显示该分类下的新闻数量"""
        return obj.news.count()
    news_count.short_description = '新闻数量'

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    """新闻管理"""
    list_display = ('title', 'category', 'author', 'status', 'views', 'is_pinned', 
                   'created_time', 'cover_preview')
    list_filter = ('status', 'category', 'is_pinned', 'created_time', 'author')
    search_fields = ('title', 'summary', 'content')
    date_hierarchy = 'created_time'
    list_editable = ('status', 'is_pinned')
    actions = ['make_published', 'make_draft', 'toggle_pin']
    readonly_fields = ('views', 'created_time', 'updated_time', 'cover_preview_large')
    fieldsets = (
        ('基本信息', {
            'fields': ('title', 'category', 'status', 'is_pinned')
        }),
        ('内容', {
            'fields': ('cover', 'cover_preview_large', 'summary', 'content')
        }),
        ('其他信息', {
            'fields': ('views', 'created_time', 'updated_time'),
            'classes': ('collapse',)
        }),
    )
    
    def cover_preview(self, obj):
        """列表中显示封面图片预览"""
        if obj.cover:
            return format_html(
                '<img src="{}" style="max-height: 50px; border-radius: 5px;"/>',
                obj.cover.url
            )
        return format_html(
            '<span style="color: #999;">无封面</span>'
        )
    cover_preview.short_description = '封面预览'
    
    def cover_preview_large(self, obj):
        """编辑页面显示大图预览"""
        if obj.cover:
            return format_html(
                '<img src="{}" style="max-height: 300px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);"/>',
                obj.cover.url
            )
        return format_html(
            '<span style="color: #999;">未上传封面图片</span>'
        )
    cover_preview_large.short_description = '封面图片预览'
    
    def make_published(self, request, queryset):
        """批量发布新闻"""
        queryset.update(status='published')
    make_published.short_description = '发布所选新闻'
    
    def make_draft(self, request, queryset):
        """批量设为草稿"""
        queryset.update(status='draft')
    make_draft.short_description = '将所选新闻设为草稿'
    
    def toggle_pin(self, request, queryset):
        """切换置顶状态"""
        for obj in queryset:
            obj.is_pinned = not obj.is_pinned
            obj.save()
    toggle_pin.short_description = '切换置顶状态'
    
    def save_model(self, request, obj, form, change):
        """保存时自动设置作者"""
        if not change:  # 新建对象时
            obj.author = request.user
        super().save_model(request, obj, form, change)

@admin.register(NewsComment)
class NewsCommentAdmin(admin.ModelAdmin):
    """新闻评论管理"""
    list_display = ('news', 'author', 'content_preview', 'created_time')
    list_filter = ('created_time', 'news', 'author')
    search_fields = ('content', 'news__title', 'author__username')
    date_hierarchy = 'created_time'
    
    def content_preview(self, obj):
        """显示评论内容预览"""
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    content_preview.short_description = '评论内容'
