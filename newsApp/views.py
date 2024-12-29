from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.urls import reverse, reverse_lazy
from .models import News, NewsCategory, NewsComment
from .forms import NewsForm, NewsCommentForm
from django.db.models import Q, F, Count

class NewsListView(ListView):
    """新闻列表视图"""
    model = News
    template_name = 'news/news_list.html'
    context_object_name = 'news_list'
    paginate_by = 10

    def get_queryset(self):
        # 基础查询：已发布的新闻
        queryset = News.objects.filter(status='published')
        
        # 搜索功能
        q = self.request.GET.get('q')
        if q:
            queryset = queryset.filter(
                Q(title__icontains=q) |
                Q(summary__icontains=q) |
                Q(content__icontains=q)
            )
        
        # 分类筛选
        category_id = self.request.GET.get('category')
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        
        # 按创建时间倒序排序，置顶新闻优先
        return queryset.order_by('-is_pinned', '-created_time')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # 添加分类列表
        context['categories'] = NewsCategory.objects.annotate(
            news_count=Count('news', filter=Q(news__status='published'))
        ).order_by('id')
        
        # 当前分类
        category_id = self.request.GET.get('category')
        if category_id:
            try:
                context['current_category'] = NewsCategory.objects.get(id=category_id)
            except NewsCategory.DoesNotExist:
                pass
        
        # 置顶新闻
        context['pinned_news'] = News.objects.filter(
            status='published',
            is_pinned=True
        ).order_by('-created_time')[:5]
        
        # 总新闻数
        context['total_news'] = News.objects.filter(status='published').count()
        
        return context

class NewsCategoryListView(ListView):
    """新闻分类列表视图"""
    model = News
    template_name = 'news/news_list.html'
    context_object_name = 'news_list'
    paginate_by = 10

    def get_queryset(self):
        self.category = get_object_or_404(NewsCategory, pk=self.kwargs['category_id'])
        return News.objects.filter(category=self.category, status='published').order_by('-created_time')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = NewsCategory.objects.all()
        context['current_category'] = self.category
        return context

class NewsDetailView(DetailView):
    """新闻详情视图"""
    model = News
    template_name = 'news/news_detail.html'
    context_object_name = 'news'

    def get_object(self):
        obj = super().get_object()
        if obj.status != 'published':
            raise Http404()
        # 增加浏览量
        obj.views = F('views') + 1
        obj.save()
        obj.refresh_from_db()
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        news = self.object
        
        # 相关新闻：同类别的最新新闻
        context['related_news'] = News.objects.filter(
            category=news.category,
            status='published'
        ).exclude(id=news.id).order_by('-created_time')[:5]
        
        # 热门新闻：浏览量最高的新闻
        context['hot_news'] = News.objects.filter(
            status='published'
        ).exclude(id=news.id).order_by('-views')[:5]
        
        context['comments'] = self.object.comments.all()
        context['comment_form'] = NewsCommentForm()
        return context

class StaffRequiredMixin(UserPassesTestMixin):
    """需要管理员权限"""
    def test_func(self):
        return self.request.user.is_staff

class NewsCreateView(LoginRequiredMixin, StaffRequiredMixin, CreateView):
    """创建新闻视图"""
    model = News
    form_class = NewsForm
    template_name = 'news/form.html'
    success_url = reverse_lazy('news:list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, '新闻创建成功！')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = '创建新闻'
        return context

class NewsUpdateView(LoginRequiredMixin, StaffRequiredMixin, UpdateView):
    """更新新闻视图"""
    model = News
    form_class = NewsForm
    template_name = 'news/form.html'
    success_url = reverse_lazy('news:list')

    def form_valid(self, form):
        messages.success(self.request, '新闻更新成功！')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = '编辑新闻'
        return context

class NewsDeleteView(LoginRequiredMixin, DeleteView):
    model = News
    success_url = reverse_lazy('news:list')
    
    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if not request.user.is_staff and obj.author != request.user:
            messages.error(request, '您没有权限删除此新闻')
            return redirect('news:detail', pk=obj.pk)
        return super().dispatch(request, *args, **kwargs)

class NewsPinView(LoginRequiredMixin, View):
    def post(self, request, pk):
        if not request.user.is_staff:
            messages.error(request, '只有管理员可以置顶新闻')
            return redirect('news:detail', pk=pk)
        
        news = get_object_or_404(News, pk=pk)
        news.is_pinned = not news.is_pinned
        news.save()
        
        action = '置顶' if news.is_pinned else '取消置顶'
        messages.success(request, f'新闻已{action}')
        return redirect('news:detail', pk=pk)

class NewsCommentCreateView(LoginRequiredMixin, CreateView):
    """创建新闻评论视图"""
    model = NewsComment
    form_class = NewsCommentForm
    http_method_names = ['post']

    def form_valid(self, form):
        news = get_object_or_404(News, pk=self.kwargs['pk'])
        form.instance.news = news
        form.instance.author = self.request.user
        response = super().form_valid(form)
        messages.success(self.request, '评论发表成功！')
        return response

    def form_invalid(self, form):
        messages.error(self.request, '评论发表失败，请检查输入。')
        return redirect(self.get_success_url())

    def get_success_url(self):
        return reverse('news:detail', kwargs={'pk': self.kwargs['pk']})

class CommentDeleteView(LoginRequiredMixin, DeleteView):
    model = NewsComment
    pk_url_kwarg = 'comment_pk'
    
    def get_success_url(self):
        return reverse('news:detail', kwargs={'pk': self.kwargs['pk']})
    
    def dispatch(self, request, *args, **kwargs):
        comment = self.get_object()
        if not request.user.is_staff and comment.author != request.user:
            messages.error(request, '您没有权限删除此评论')
            return redirect('news:detail', pk=self.kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)

class AddCommentView(LoginRequiredMixin, View):
    """添加新闻评论视图"""
    def post(self, request, pk):
        news = get_object_or_404(News, pk=pk)
        content = request.POST.get('content', '').strip()
        
        if not content:
            messages.error(request, '评论内容不能为空')
            return redirect('news:detail', pk=pk)
        
        # 创建评论
        NewsComment.objects.create(
            news=news,
            user=request.user,
            content=content
        )
        
        messages.success(request, '评论发布成功')
        return redirect('news:detail', pk=pk)
