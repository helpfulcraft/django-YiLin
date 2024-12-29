from django.urls import path
from . import views

app_name = 'service'

urlpatterns = [
    # 服务列表和详情
    path('', views.ServiceListView.as_view(), name='list'),
    path('<int:pk>/', views.ServiceDetailView.as_view(), name='detail'),
    
    # 服务预约
    path('<int:pk>/appointment/', views.AppointmentCreateView.as_view(), name='make_appointment'),
    path('appointments/', views.AppointmentListView.as_view(), name='appointment_list'),
    path('appointments/<int:pk>/', views.AppointmentDetailView.as_view(), name='appointment_detail'),
    path('appointments/<int:pk>/cancel/', views.AppointmentCancelView.as_view(), name='appointment_cancel'),
    
    # 服务评价
    path('<int:pk>/review/', views.ReviewCreateView.as_view(), name='review_create'),
    path('<int:pk>/reviews/', views.ReviewListView.as_view(), name='review_list'),
]
