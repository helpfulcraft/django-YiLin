from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy, reverse
from django.db.models import Q
from .models import Service, ServiceCategory, ServiceAppointment, ServiceReview
from .forms import ServiceAppointmentForm, ServiceReviewForm

class ServiceListView(ListView):
    """服务列表视图"""
    model = Service
    template_name = 'service/service_list.html'
    context_object_name = 'services'
    paginate_by = 9

    def get_queryset(self):
        queryset = Service.objects.all()
        
        # 搜索功能
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(name__icontains=query) |
                Q(short_description__icontains=query) |
                Q(content__icontains=query)
            )
        
        # 分类过滤
        category = self.request.GET.get('category')
        if category:
            queryset = queryset.filter(category_id=category)
            
        return queryset.order_by('-created_time')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = ServiceCategory.objects.all()
        context['current_category'] = self.request.GET.get('category')
        context['query'] = self.request.GET.get('q', '')
        return context

class ServiceDetailView(DetailView):
    """服务详情视图"""
    model = Service
    template_name = 'service/service_detail.html'
    context_object_name = 'service'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Debug print
        print(f"Service ID: {self.object.id}")
        print(f"Service Name: {self.object.name}")
        
        # Fetch reviews
        reviews = self.object.reviews.select_related('user').all()
        context['reviews'] = reviews
        
        # Review form for authenticated users
        if self.request.user.is_authenticated:
            context['review_form'] = ServiceReviewForm()
            context['appointment_form'] = ServiceAppointmentForm()
        
        return context

class AppointmentCreateView(LoginRequiredMixin, CreateView):
    """创建预约视图"""
    model = ServiceAppointment
    form_class = ServiceAppointmentForm
    template_name = 'service/appointment_form.html'
    
    def get_success_url(self):
        return reverse('service:appointment_detail', kwargs={'pk': self.object.pk})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['service'] = get_object_or_404(Service, pk=self.kwargs['pk'])
        return context
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.service = get_object_or_404(Service, pk=self.kwargs['pk'])
        messages.success(self.request, '预约申请已提交，请等待确认！')
        return super().form_valid(form)

class AppointmentListView(LoginRequiredMixin, ListView):
    """预约列表视图"""
    model = ServiceAppointment
    template_name = 'service/appointment_list.html'
    context_object_name = 'appointments'
    
    def get_queryset(self):
        return ServiceAppointment.objects.filter(user=self.request.user).select_related('service')

class AppointmentDetailView(LoginRequiredMixin, DetailView):
    """预约详情视图"""
    model = ServiceAppointment
    template_name = 'service/appointment_detail.html'
    context_object_name = 'appointment'

class AppointmentCancelView(LoginRequiredMixin, DeleteView):
    """取消预约视图"""
    model = ServiceAppointment
    success_url = reverse_lazy('service:appointment_list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, '预约已取消！')
        return super().delete(request, *args, **kwargs)

class ReviewCreateView(LoginRequiredMixin, CreateView):
    """创建评价视图"""
    model = ServiceReview
    form_class = ServiceReviewForm
    template_name = 'service/review_form.html'
    
    def get_success_url(self):
        return reverse('service:detail', kwargs={'pk': self.kwargs['pk']})
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.service = get_object_or_404(Service, pk=self.kwargs['pk'])
        messages.success(self.request, '评价已提交，感谢您的反馈！')
        return super().form_valid(form)

class ReviewListView(ListView):
    """评价列表视图"""
    model = ServiceReview
    template_name = 'service/review_list.html'
    context_object_name = 'reviews'
    
    def get_queryset(self):
        service = get_object_or_404(Service, pk=self.kwargs['pk'])
        return service.reviews.select_related('user').all()

class ServiceCategoryView(ListView):
    """服务类别视图"""
    model = ServiceCategory
    template_name = 'service/service_category.html'
    context_object_name = 'categories'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        for category in context['categories']:
            category.service_count = category.services.count()
        return context

class ServiceHomeCareView(ListView):
    """居家养老服务视图"""
    model = Service
    template_name = 'service/service_home_care.html'
    context_object_name = 'services'

    def get_queryset(self):
        return Service.objects.filter(category__name='居家养老').order_by('-created_time')

class ServiceCommunityCareView(ListView):
    """社区照护服务视图"""
    model = Service
    template_name = 'service/service_community_care.html'
    context_object_name = 'services'

    def get_queryset(self):
        return Service.objects.filter(category__name='社区照护').order_by('-created_time')

class ServiceInstitutionalCareView(ListView):
    """机构养老服务视图"""
    model = Service
    template_name = 'service/service_institutional_care.html'
    context_object_name = 'services'

    def get_queryset(self):
        return Service.objects.filter(category__name='机构养老').order_by('-created_time')

class ServiceMedicalCareView(ListView):
    """医养结合服务视图"""
    model = Service
    template_name = 'service/service_medical_care.html'
    context_object_name = 'services'

    def get_queryset(self):
        return Service.objects.filter(category__name='医养结合').order_by('-created_time')
