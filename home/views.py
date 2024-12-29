from django.shortcuts import render
from django.views.generic import TemplateView, ListView
from django.db.models import Q, Count, Sum, F
from django.utils import timezone
from .models import Banner, Statistics
from newsApp.models import News
from volunteerApp.models import VolunteerActivity, VolunteerProfile
from serviceApp.models import Service
from userApp.models import UserProfile
from django.db import models

class HomeView(TemplateView):
    template_name = 'home/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # 获取轮播图数据
        context['banners'] = Banner.objects.filter(
            is_active=True,
            start_time__lte=timezone.now(),
            end_time__gte=timezone.now()
        ).order_by('order')[:5]
        
        # 获取统计数据
        context['statistics'] = [
            {
                'title': '注册用户',
                'value': UserProfile.objects.count(),
                'icon': 'bi bi-people'
            },
            {
                'title': '志愿者活动',
                'value': VolunteerActivity.objects.count(),
                'icon': 'bi bi-heart'
            },
            {
                'title': '服务项目',
                'value': Service.objects.count(),
                'icon': 'bi bi-briefcase'
            },
            {
                'title': '累计服务时长',
                'value': sum(
                    (activity.end_time - activity.start_time).total_seconds() / 3600
                    for activity in VolunteerActivity.objects.filter(status='closed')
                ) + (128 * 20),  # 实际时长（小时）+ 基础时长
                'icon': 'bi bi-clock'
            }
        ]
        
        # 获取推荐活动
        context['activities'] = VolunteerActivity.objects.filter(
            status='recruiting',
            start_time__gte=timezone.now()
        ).order_by('-created_time')[:4]
        
        # 获取最新新闻
        context['latest_news'] = News.objects.filter(
            status='published'
        ).order_by('-created_time')[:3]
        
        # 获取特色服务
        context['featured_services'] = Service.objects.filter(
            status='active',
            is_featured=True
        ).order_by('-created_time')[:3]
        
        # 获取推荐活动（即将开始且名额未满的活动）
        context['featured_activities'] = VolunteerActivity.objects.filter(
            status='published'
        ).exclude(
            current_volunteers__gte=F('required_volunteers')  # 排除已满的活动
        ).order_by('start_time')[:4]  # 按开始时间排序，优先显示即将开始的活动
        
        return context

class SearchView(ListView):
    template_name = 'home/search.html'
    context_object_name = 'results'
    paginate_by = 10

    def get_queryset(self):
        query = self.request.GET.get('q', '')
        if not query:
            return []

        news = News.objects.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(summary__icontains=query),
            status='published'
        ).order_by('-created_time')

        activities = VolunteerActivity.objects.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query),
            status='recruiting'
        ).order_by('-created_time')

        services = Service.objects.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query),
            is_active=True
        ).order_by('-created_time')

        # 合并查询结果
        results = list(news) + list(activities) + list(services)
        results.sort(key=lambda x: x.created_time, reverse=True)
        
        return results

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')
        return context
