from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'user'

urlpatterns = [
    # 用户认证
    path('login/', auth_views.LoginView.as_view(template_name='user/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home:home'), name='logout'),
    path('register/', views.register, name='register'),
    
    # 用户资料
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.profile_edit, name='profile_edit'),
    path('avatar/', views.update_avatar, name='update_avatar'),
    
    # 邮箱验证
    path('resend-verification/', views.resend_verification, name='resend_verification'),
    path('verify-email/<str:uidb64>/<str:token>/', views.verify_email, name='verify_email'),
    
    # 身份验证
    path('verify-identity/', views.verify_identity, name='verify_identity'),
    
    # 健康信息
    path('health-info/', views.health_info, name='health_info'),
    
    # 紧急联系人
    path('emergency-contacts/', views.emergency_contacts, name='emergency_contacts'),
    path('emergency-contacts/add/', views.add_emergency_contact, name='add_emergency_contact'),
    path('emergency-contacts/edit/<int:contact_id>/', views.edit_emergency_contact, name='edit_emergency_contact'),
    path('emergency-contacts/delete/<int:contact_id>/', views.delete_emergency_contact, name='delete_emergency_contact'),
    
    # 服务记录
    path('service-history/', views.service_history, name='service_history'),
    
    # 志愿服务记录
    path('volunteer-history/', views.volunteer_history, name='volunteer_history'),
    
    # 通知
    path('notifications/', views.notifications, name='notifications'),
    path('notifications/mark-read/<int:notification_id>/', views.mark_notification_read, name='mark_notification_read'),
    path('notifications/mark-all-read/', views.mark_all_notifications_read, name='mark_all_notifications_read'),
]
