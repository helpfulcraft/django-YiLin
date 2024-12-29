from django.urls import path
from . import views

app_name = 'volunteer'

urlpatterns = [
    # 活动列表和详情
    path('', views.ActivityListView.as_view(), name='activity_list'),
    path('activity/<int:pk>/', views.ActivityDetailView.as_view(), name='activity_detail'),
    
    # 活动管理
    path('create/', views.ActivityCreateView.as_view(), name='create_activity'),
    path('<int:pk>/edit/', views.ActivityUpdateView.as_view(), name='edit_activity'),
    path('<int:pk>/delete/', views.ActivityDeleteView.as_view(), name='delete_activity'),
    
    # 报名管理
    path('activity/<int:pk>/apply/', views.ActivityApplyView.as_view(), name='activity_apply'),
    path('<int:pk>/applications/', views.ManageApplicationsView.as_view(), name='manage_applications'),
    path('applications/<int:pk>/update/', views.UpdateApplicationStatusView.as_view(), name='update_application'),
    path('applications/<int:pk>/cancel/', views.CancelApplicationView.as_view(), name='cancel_application'),
    
    # 评论
    path('activity/<int:pk>/comment/', views.add_activity_comment, name='add_comment'),
    
    # 志愿者档案
    path('profile/', views.VolunteerProfileView.as_view(), name='profile'),
]
