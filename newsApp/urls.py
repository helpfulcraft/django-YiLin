from django.urls import path
from .views import (
    NewsListView, NewsDetailView, NewsCreateView, 
    NewsUpdateView, NewsDeleteView, NewsCommentCreateView,
    CommentDeleteView, NewsCategoryListView, NewsPinView,
    AddCommentView
)

app_name = 'news'

urlpatterns = [
    # 新闻浏览
    path('', NewsListView.as_view(), name='list'),
    path('<int:pk>/', NewsDetailView.as_view(), name='detail'),
    path('category/<int:category_id>/', NewsCategoryListView.as_view(), name='category'),
    
    # 新闻管理
    path('create/', NewsCreateView.as_view(), name='create'),
    path('<int:pk>/edit/', NewsUpdateView.as_view(), name='edit'),
    path('<int:pk>/delete/', NewsDeleteView.as_view(), name='delete'),
    path('<int:pk>/pin/', NewsPinView.as_view(), name='pin'),
    
    # 评论管理
    path('<int:pk>/comment/add/', NewsCommentCreateView.as_view(), name='comment_add'),
    path('<int:pk>/comment/<int:comment_pk>/delete/', CommentDeleteView.as_view(), name='comment_delete'),
    path('<int:pk>/add_comment/', AddCommentView.as_view(), name='add_comment'),
]
