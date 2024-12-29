from django.urls import path
from . import views

app_name = 'home'

urlpatterns = [
    path('', views.home, name='home'),
    path('search/', views.site_search, name='search'),
    path('carousel/<int:pk>/', views.carousel_detail, name='carousel_detail'),
]
