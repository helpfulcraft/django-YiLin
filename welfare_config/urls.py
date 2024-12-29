"""welfare URL Configuration"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),  
    path('user/', include('userApp.urls')),
    path('volunteer/', include('volunteerApp.urls')),
    path('news/', include('newsApp.urls')),
    path('service/', include('serviceApp.urls')),
    path('help/', include('helpApp.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('favicon.ico', RedirectView.as_view(url='/static/images/favicon.ico')),
]

if settings.DEBUG:
    urlpatterns += [
        path('__debug__/', include('debug_toolbar.urls')),
    ]
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
