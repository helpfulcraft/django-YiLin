from django.urls import path
from . import views

app_name = 'volunteer'

urlpatterns = [
    path('', views.home, name='home'),
    path('activities/', views.activity_list, name='activity_list'),
    path('activities/<int:pk>/', views.activity_detail, name='activity_detail'),
    path('activities/create/', views.create_activity, name='create_activity'),
    path('my-applications/', views.my_applications, name='my_applications'),
]
