from django.shortcuts import render, get_object_or_404
from django.db.models import Q, Sum, Count
from django.contrib.auth import get_user_model
from newsApp.models import News
from volunteerApp.models import VolunteerActivity
from serviceApp.models import Service
from .models import Carousel

def home(request):
    """首页视图"""
    User = get_user_model()
    
    context = {
        'stats': {
            'user_count': User.objects.count(),
            'activity_count': VolunteerActivity.objects.filter(status='active').count(),
            'service_count': Service.objects.filter(status='active').count(),
            'service_hours': VolunteerActivity.objects.filter(
                status='completed'
            ).aggregate(
                total_hours=Sum('duration')
            ).get('total_hours', 0) or 0
        },
        'news_list': News.objects.filter(
            status='published'
        ).order_by('-created_time')[:5],
        'activities': VolunteerActivity.objects.filter(
            status='active'
        ).order_by('-created_time')[:5],
        'services': Service.objects.filter(
            status='active'
        ).order_by('-created_time')[:5],
        'carousels': Carousel.objects.filter(is_active=True).order_by('order')[:5],
    }
    return render(request, 'home/home.html', context)

def site_search(request):
    """站内搜索"""
    query = request.GET.get('q', '')
    context = {
        'query': query,
        'news_list': [],
        'activities': [],
        'services': []
    }
    
    if query:
        context.update({
            'news_list': News.objects.filter(
                Q(title__icontains=query) |
                Q(content__icontains=query)
            )[:5],
            'activities': VolunteerActivity.objects.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query)
            )[:5],
            'services': Service.objects.filter(
                Q(name__icontains=query) |
                Q(description__icontains=query)
            )[:5]
        })
    
    return render(request, 'home/search.html', context)

def carousel_detail(request, pk):
    """轮播图详情"""
    carousel = get_object_or_404(Carousel, pk=pk)
    return render(request, 'home/carousel_detail.html', {'carousel': carousel})
