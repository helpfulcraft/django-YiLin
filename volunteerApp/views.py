from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse_lazy, reverse
from django.db.models import Q, Sum, Count
from .models import VolunteerActivity, VolunteerApplication, ActivityCategory, ActivityComment
from .forms import ActivityForm, ApplicationForm
from django.utils import timezone

class ActivityListView(ListView):
    """志愿活动列表视图"""
    model = VolunteerActivity
    template_name = 'volunteer/activity_list.html'
    context_object_name = 'activities'
    paginate_by = 12
    
    def get_queryset(self):
        queryset = VolunteerActivity.objects.filter(status='published')
        category_id = self.request.GET.get('category')
        query = self.request.GET.get('q')
        
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query)
            )
        return queryset.order_by('-created_time')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = ActivityCategory.objects.all().order_by('order')
        context['current_category'] = self.request.GET.get('category')
        
        # 计算志愿者总人数（已通过审核的报名）
        registered_volunteers = VolunteerApplication.objects.filter(
            status='approved'
        ).values('user').distinct().count()
        # 添加基础志愿者数量
        context['total_volunteers'] = registered_volunteers + 128
        
        # 计算总服务时长（已完成的活动）
        completed_activities = VolunteerActivity.objects.filter(
            status='completed'
        )
        actual_hours = sum(activity.duration for activity in completed_activities if activity.duration)
        # 添加基础服务时长（按平均每个志愿者服务20小时计算）
        base_hours = 128 * 20  # 基础志愿者 * 平均服务时长
        context['total_hours'] = actual_hours + base_hours
        
        # 添加当前进行中的活动数量
        context['ongoing_activities'] = VolunteerActivity.objects.filter(
            status='published',
            end_time__gte=timezone.now()
        ).count() + 15  # 添加一些基础数量
        
        return context

class ActivityDetailView(DetailView):
    """志愿活动详情视图"""
    model = VolunteerActivity
    template_name = 'volunteer/activity_detail.html'
    context_object_name = 'activity'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        activity = self.get_object()
        user = self.request.user

        # 获取用户的报名状态
        if user.is_authenticated:
            context['application'] = VolunteerApplication.objects.filter(
                user=user,
                activity=activity
            ).first()
            
            # 检查用户是否参与过该活动
            context['user_participated'] = VolunteerApplication.objects.filter(
                user=user,
                activity=activity,
                status='approved',
                activity__end_time__lt=timezone.now()
            ).exists()

            # 获取用户的评论
            context['user_comment'] = ActivityComment.objects.filter(
                user=user,
                activity=activity
            ).first()

        # 获取活动评论
        context['comments'] = ActivityComment.objects.filter(
            activity=activity
        ).select_related('user').order_by('-created_time')

        # 获取相关活动（同一分类的其他活动）
        if activity.category:
            context['related_activities'] = VolunteerActivity.objects.filter(
                category=activity.category,
                status='published'
            ).exclude(
                id=activity.id
            ).order_by('-created_time')[:5]

        # 获取活动统计信息
        context['total_applications'] = activity.applications.count()
        context['approved_applications'] = activity.applications.filter(status='approved').count()
        context['remaining_spots'] = max(0, activity.required_volunteers - context['approved_applications'])

        return context

class ActivityCreateView(LoginRequiredMixin, CreateView):
    """创建志愿活动视图"""
    model = VolunteerActivity
    form_class = ActivityForm
    template_name = 'volunteer/activity_form.html'
    
    def get_success_url(self):
        return reverse('volunteer:activity_detail', kwargs={'pk': self.object.pk})
    
    def form_valid(self, form):
        form.instance.organizer = self.request.user
        messages.success(self.request, '活动创建成功！')
        return super().form_valid(form)

class ActivityUpdateView(LoginRequiredMixin, UpdateView):
    """更新志愿活动视图"""
    model = VolunteerActivity
    form_class = ActivityForm
    template_name = 'volunteer/activity_form.html'
    
    def get_success_url(self):
        return reverse('volunteer:activity_detail', kwargs={'pk': self.object.pk})
    
    def form_valid(self, form):
        messages.success(self.request, '活动更新成功！')
        return super().form_valid(form)

class ActivityDeleteView(LoginRequiredMixin, DeleteView):
    """删除志愿活动视图"""
    model = VolunteerActivity
    success_url = reverse_lazy('volunteer:activity_list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, '活动已删除！')
        return super().delete(request, *args, **kwargs)

class ActivityApplyView(LoginRequiredMixin, CreateView):
    """活动报名视图"""
    model = VolunteerApplication
    template_name = 'volunteer/activity_apply.html'
    fields = ['message']
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['activity'] = get_object_or_404(VolunteerActivity, pk=self.kwargs['pk'])
        return context
    
    def get_success_url(self):
        return reverse('volunteer:activity_detail', kwargs={'pk': self.kwargs['pk']})
    
    def form_valid(self, form):
        activity = get_object_or_404(VolunteerActivity, pk=self.kwargs['pk'])
        form.instance.user = self.request.user
        form.instance.activity = activity
        
        # Check if user has already applied
        existing_application = VolunteerApplication.objects.filter(
            user=self.request.user, 
            activity=activity
        ).exists()
        
        if existing_application:
            messages.error(self.request, '您已经申请过此活动')
            return redirect('volunteer:activity_detail', pk=activity.pk)
        
        # Check if activity is full
        if activity.is_full():
            messages.error(self.request, '活动名额已满')
            return redirect('volunteer:activity_detail', pk=activity.pk)
        
        response = super().form_valid(form)
        messages.success(self.request, '申请成功！')
        return response

class ManageApplicationsView(LoginRequiredMixin, ListView):
    """管理活动报名视图"""
    model = VolunteerApplication
    template_name = 'volunteer/manage_applications.html'
    context_object_name = 'applications'
    
    def get_queryset(self):
        activity = get_object_or_404(VolunteerActivity, pk=self.kwargs['pk'])
        if self.request.user != activity.organizer:
            return VolunteerApplication.objects.none()
        return activity.applications.select_related('user').all()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['activity'] = get_object_or_404(VolunteerActivity, pk=self.kwargs['pk'])
        return context

class UpdateApplicationStatusView(LoginRequiredMixin, View):
    """更新报名状态视图"""
    def post(self, request, pk):
        application = get_object_or_404(VolunteerApplication, pk=pk)
        
        # 确保只有活动组织者可以更新申请状态
        if request.user != application.activity.organizer:
            messages.error(request, '您没有权限更新此申请状态')
            return redirect('volunteer:manage_applications', pk=application.activity.pk)
        
        new_status = request.POST.get('status')
        if new_status in dict(VolunteerApplication.STATUS_CHOICES):
            application.status = new_status
            application.save()
            
            # 更新活动的志愿者数量
            application.activity.save()
            
            if new_status == 'approved':
                messages.success(request, '申请已通过')
            elif new_status == 'rejected':
                messages.warning(request, '申请已拒绝')
        
        return redirect('volunteer:manage_applications', pk=application.activity.pk)

class CancelApplicationView(LoginRequiredMixin, View):
    """取消报名视图"""
    def post(self, request, pk):
        application = get_object_or_404(VolunteerApplication, activity__pk=pk, user=request.user)
        activity_pk = application.activity.pk
        application.delete()
        messages.success(request, '报名已取消！')
        return redirect('volunteer:activity_detail', pk=activity_pk)

class VolunteerProfileView(LoginRequiredMixin, DetailView):
    """志愿者档案视图"""
    model = VolunteerApplication
    template_name = 'volunteer/profile.html'
    
    def get_object(self):
        return self.request.user
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['applications'] = VolunteerApplication.objects.filter(
            user=self.request.user
        ).select_related('activity').order_by('-created_at')
        return context

@login_required
def add_activity_comment(request, pk):
    """添加活动评论"""
    activity = get_object_or_404(VolunteerActivity, pk=pk)
    
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            # 检查用户是否参与过该活动
            participated = VolunteerApplication.objects.filter(
                volunteer=request.user,
                activity=activity,
                status='approved',
                activity__end_time__lt=timezone.now()
            ).exists()
            
            if participated:
                # 检查用户是否已经评论过
                existing_comment = ActivityComment.objects.filter(
                    user=request.user,
                    activity=activity
                ).first()
                
                if not existing_comment:
                    ActivityComment.objects.create(
                        activity=activity,
                        user=request.user,
                        content=content
                    )
                    messages.success(request, '评论发表成功！')
                else:
                    messages.error(request, '您已经评论过该活动')
            else:
                messages.error(request, '只有参与过活动的志愿者才能发表评论')
        else:
            messages.error(request, '评论内容不能为空')
    
    return redirect('volunteer:activity_detail', pk=pk)
