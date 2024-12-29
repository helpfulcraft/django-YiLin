from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.db.models import Q
from .models import HelpCategory, HelpArticle, FAQ, Guide, Feedback, OnlineConsultation
from .forms import FeedbackForm, ConsultationForm

class HelpCenterView(ListView):
    """帮助中心首页"""
    model = HelpCategory
    template_name = 'help/help_center.html'
    context_object_name = 'categories'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # 获取热门文章（按浏览量排序）
        context['popular_articles'] = HelpArticle.objects.filter(
            is_published=True
        ).order_by('-views')[:5]
        
        # 获取最新FAQ
        context['recent_faqs'] = FAQ.objects.filter(
            is_published=True
        ).order_by('-created_time')[:5]
        
        # 获取使用指南
        context['guides'] = Guide.objects.filter(
            is_published=True
        ).order_by('order', '-created_time')[:6]
        
        # 获取最新反馈（已解决的）
        context['solved_feedbacks'] = Feedback.objects.filter(
            status='resolved'
        ).order_by('-updated_time')[:5]
        
        return context

class AboutView(TemplateView):
    """关于我们页面"""
    template_name = 'help/about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = '关于我们'
        context['description'] = '福祉网站致力于为社会提供优质的志愿服务，促进社会和谐发展。'
        return context

class HelpArticleDetailView(DetailView):
    """帮助文章详情页"""
    model = HelpArticle
    template_name = 'help/article.html'
    context_object_name = 'article'

    def get_object(self):
        obj = super().get_object()
        if not self.request.user.is_staff:
            obj.views += 1
            obj.save()
        return obj

def help_search(request):
    """帮助搜索"""
    query = request.GET.get('q', '')
    if query:
        articles = HelpArticle.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query),
            is_published=True
        )
        faqs = FAQ.objects.filter(
            Q(question__icontains=query) | Q(answer__icontains=query),
            is_published=True
        )
        guides = Guide.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query),
            is_published=True
        )
    else:
        articles = HelpArticle.objects.none()
        faqs = FAQ.objects.none()
        guides = Guide.objects.none()

    context = {
        'query': query,
        'articles': articles,
        'faqs': faqs,
        'guides': guides,
    }
    return render(request, 'help/search.html', context)

class FAQListView(ListView):
    """常见问题列表"""
    model = FAQ
    template_name = 'help/faq.html'
    context_object_name = 'faqs'
    paginate_by = 10

    def get_queryset(self):
        queryset = FAQ.objects.filter(is_published=True)
        category_id = self.request.GET.get('category')
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        return queryset.order_by('order', '-created_time')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = HelpCategory.objects.all()
        context['selected_category'] = None
        category_id = self.request.GET.get('category')
        if category_id:
            context['selected_category'] = get_object_or_404(HelpCategory, id=category_id)
        return context

class FAQDetailView(DetailView):
    """常见问题详情"""
    model = FAQ
    template_name = 'help/faq_detail.html'
    context_object_name = 'faq'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['related_faqs'] = FAQ.objects.filter(
            category=self.object.category,
            is_published=True
        ).exclude(id=self.object.id)[:5]
        return context

class GuideListView(ListView):
    """使用指南列表"""
    model = Guide
    template_name = 'help/guide.html'
    context_object_name = 'guides'
    paginate_by = 10

    def get_queryset(self):
        queryset = Guide.objects.filter(is_published=True)
        category_id = self.request.GET.get('category')
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        return queryset.order_by('order', '-created_time')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = HelpCategory.objects.all()
        context['selected_category'] = None
        category_id = self.request.GET.get('category')
        if category_id:
            context['selected_category'] = get_object_or_404(HelpCategory, id=category_id)
        return context

class GuideDetailView(DetailView):
    """使用指南详情"""
    model = Guide
    template_name = 'help/guide_detail.html'
    context_object_name = 'guide'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['related_guides'] = Guide.objects.filter(
            category=self.object.category,
            is_published=True
        ).exclude(id=self.object.id)[:5]
        return context

class HelpCategoryView(ListView):
    """帮助分类视图"""
    model = HelpArticle
    template_name = 'help/category.html'
    context_object_name = 'articles'
    paginate_by = 10

    def get_queryset(self):
        category_id = self.kwargs.get('pk')
        return HelpArticle.objects.filter(category_id=category_id, is_published=True).order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_id = self.kwargs.get('pk')
        context['category'] = get_object_or_404(HelpCategory, pk=category_id)
        return context

class FeedbackListView(LoginRequiredMixin, ListView):
    """反馈列表"""
    model = Feedback
    template_name = 'help/feedback_list.html'
    context_object_name = 'feedbacks'
    paginate_by = 10

    def get_queryset(self):
        return Feedback.objects.filter(user=self.request.user).order_by('-created_time')

class FeedbackCreateView(LoginRequiredMixin, CreateView):
    """创建反馈"""
    model = Feedback
    form_class = FeedbackForm
    template_name = 'help/feedback_form.html'
    success_url = reverse_lazy('help:feedback_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, '反馈提交成功！')
        return super().form_valid(form)

class FeedbackDetailView(LoginRequiredMixin, DetailView):
    """反馈详情"""
    model = Feedback
    template_name = 'help/feedback_detail.html'
    context_object_name = 'feedback'

    def get_queryset(self):
        return Feedback.objects.filter(user=self.request.user)

class OnlineConsultationListView(LoginRequiredMixin, ListView):
    """在线咨询列表"""
    model = OnlineConsultation
    template_name = 'help/consultation_list.html'
    context_object_name = 'consultations'
    paginate_by = 10

    def get_queryset(self):
        return OnlineConsultation.objects.filter(user=self.request.user).order_by('-created_time')

class OnlineConsultationCreateView(LoginRequiredMixin, CreateView):
    """创建在线咨询"""
    model = OnlineConsultation
    form_class = ConsultationForm
    template_name = 'help/consultation_form.html'
    success_url = reverse_lazy('help:consultation_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, '咨询提交成功！')
        return super().form_valid(form)

class OnlineConsultationDetailView(LoginRequiredMixin, DetailView):
    """在线咨询详情"""
    model = OnlineConsultation
    template_name = 'help/consultation_detail.html'
    context_object_name = 'consultation'

    def get_queryset(self):
        return OnlineConsultation.objects.filter(user=self.request.user)
