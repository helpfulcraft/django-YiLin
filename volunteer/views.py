from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Activity, Application
from .forms import ActivityForm, ApplicationForm

def home(request):
    """首页"""
    # 获取最近的3个活动
    recent_activities = Activity.objects.all()[:3]
    return render(request, 'volunteer/home.html', {
        'recent_activities': recent_activities
    })

def activity_list(request):
    """活动列表页面"""
    # 获取所有活动
    activities = Activity.objects.all()
    return render(request, 'volunteer/activity_list.html', {
        'activities': activities
    })

def activity_detail(request, pk):
    """活动详情页面"""
    # 获取活动详情
    activity = get_object_or_404(Activity, pk=pk)
    
    # 检查用户是否已经申请过
    user_application = None
    if request.user.is_authenticated:
        user_application = Application.objects.filter(user=request.user, activity=activity).first()
    
    # 处理申请提交
    if request.method == 'POST' and request.user.is_authenticated:
        if user_application:
            messages.warning(request, '您已经申请过这个活动了！')
            return redirect('activity_detail', pk=pk)
            
        form = ApplicationForm(request.POST)
        if form.is_valid():
            # 保存申请
            application = form.save(commit=False)
            application.user = request.user
            application.activity = activity
            application.save()
            messages.success(request, '申请提交成功！')
            return redirect('activity_detail', pk=pk)
    else:
        # 初始化申请表单
        form = ApplicationForm()
    
    return render(request, 'volunteer/activity_detail.html', {
        'activity': activity,
        'form': form,
        'user_application': user_application
    })

@login_required
def my_applications(request):
    """我的申请列表"""
    # 获取用户的所有申请
    applications = Application.objects.filter(user=request.user)
    return render(request, 'volunteer/my_applications.html', {
        'applications': applications
    })

@login_required
def create_activity(request):
    """创建活动"""
    # 检查用户是否是管理员
    if not request.user.is_staff:
        messages.error(request, '只有管理员才能创建活动')
        return redirect('activity_list')
        
    # 处理活动创建
    if request.method == 'POST':
        form = ActivityForm(request.POST)
        if form.is_valid():
            # 保存活动
            activity = form.save()
            messages.success(request, '活动创建成功！')
            return redirect('activity_detail', pk=activity.pk)
    else:
        # 初始化活动表单
        form = ActivityForm()
    
    return render(request, 'volunteer/create_activity.html', {
        'form': form
    })
