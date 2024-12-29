from django.urls import path
from . import views

app_name = 'help'

urlpatterns = [
    # 帮助中心首页
    path('', views.HelpCenterView.as_view(), name='help_center'),
    
    # 搜索
    path('search/', views.help_search, name='search'),
    
    # 帮助文章
    path('article/<int:pk>/', views.HelpArticleDetailView.as_view(), name='article'),
    path('category/<int:pk>/', views.HelpCategoryView.as_view(), name='category'),
    
    # FAQ
    path('faq/', views.FAQListView.as_view(), name='faq'),
    path('faq/<int:pk>/', views.FAQDetailView.as_view(), name='faq_detail'),
    
    # 使用指南
    path('guide/', views.GuideListView.as_view(), name='guide'),
    path('guide/<int:pk>/', views.GuideDetailView.as_view(), name='guide_detail'),
    
    # 反馈
    path('feedback/', views.FeedbackListView.as_view(), name='feedback_list'),
    path('feedback/create/', views.FeedbackCreateView.as_view(), name='feedback_create'),
    path('feedback/<int:pk>/', views.FeedbackDetailView.as_view(), name='feedback_detail'),
    
    # 在线咨询
    path('consultation/', views.OnlineConsultationListView.as_view(), name='consultation_list'),
    path('consultation/create/', views.OnlineConsultationCreateView.as_view(), name='consultation_create'),
    path('consultation/<int:pk>/', views.OnlineConsultationDetailView.as_view(), name='consultation_detail'),
    
    # 关于我们
    path('about/', views.AboutView.as_view(), name='about'),
]
