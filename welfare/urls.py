"""welfare URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('homeApp.urls')),  # 首页应用
    path('user/', include('userApp.urls')),  # 用户系统
    path('news/', include('newsApp.urls')),  # 新闻系统
    path('volunteer/', include('volunteerApp.urls')),  # 志愿者系统
    path('service/', include('serviceApp.urls')),  # 服务系统
    path('help/', include('helpApp.urls')),  # 帮助中心
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # 添加媒体文件的URL配置