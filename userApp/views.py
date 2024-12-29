from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import login
from .forms import UserRegistrationForm, UserProfileForm
from .models import UserProfile, Notification, EmergencyContact, HealthInfo
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User
from serviceApp.models import ServiceAppointment
from volunteerApp.models import VolunteerApplication
import logging
logger = logging.getLogger(__name__)

def register(request):
    """用户注册视图"""
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
                UserProfile.objects.create(user=user)  # 创建用户资料
                login(request, user)
                messages.success(request, '注册成功！')
                return redirect('user:profile')
            except Exception as e:
                messages.error(request, f'注册失败：{str(e)}')
        else:
            messages.error(request, '注册失败，请检查输入信息。')
    else:
        form = UserRegistrationForm()
    return render(request, 'user/register.html', {'form': form})

@login_required
def profile(request):
    """用户资料视图"""
    try:
        if request.method == 'POST':
            form = UserProfileForm(request.POST, request.FILES, instance=request.user.userprofile)
            if form.is_valid():
                form.save()
                messages.success(request, '资料更新成功！')
                return redirect('user:profile')
            else:
                messages.error(request, '更新失败，请检查输入信息。')
                logger.error(f'表单验证失败: {form.errors}')
        else:
            form = UserProfileForm(instance=request.user.userprofile)
        
        # 获取最近的服务记录和志愿记录
        logger.info(f'开始获取用户 {request.user.username} 的服务记录')
        service_records = ServiceAppointment.objects.filter(user=request.user).order_by('-created_time')[:5]
        logger.info(f'服务记录数量: {service_records.count()}')
        for record in service_records:
            logger.debug(f'服务记录: {record.service.name} - {record.status}')

        logger.info(f'开始获取用户 {request.user.username} 的志愿记录')
        volunteer_records = VolunteerApplication.objects.filter(
            user=request.user,
            status='approved'
        ).order_by('-created_time')[:5]
        logger.info(f'志愿记录数量: {volunteer_records.count()}')
        for record in volunteer_records:
            logger.debug(f'志愿记录: {record.activity.title} - {record.status}')
        
        context = {
            'form': form,
            'user': request.user,
            'service_records': service_records,
            'volunteer_records': volunteer_records
        }
        logger.info('准备渲染模板')
        return render(request, 'user/profile.html', context)
    except Exception as e:
        logger.error(f'视图发生错误: {str(e)}', exc_info=True)
        messages.error(request, f'发生错误：{str(e)}')
        return redirect('home:home')

@login_required
def profile_edit(request):
    """编辑用户资料视图"""
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user.userprofile)
        if form.is_valid():
            form.save()
            messages.success(request, '资料更新成功！')
            return redirect('user:profile')
        else:
            messages.error(request, '更新失败，请检查输入信息。')
    else:
        form = UserProfileForm(instance=request.user.userprofile)
    return render(request, 'user/profile_edit.html', {'form': form})

@login_required
def update_avatar(request):
    """更新头像视图"""
    try:
        if request.method == 'POST' and request.FILES.get('avatar'):
            request.user.userprofile.avatar = request.FILES['avatar']
            request.user.userprofile.save()
            messages.success(request, '头像更新成功！')
        else:
            messages.error(request, '请选择要上传的头像文件。')
    except Exception as e:
        messages.error(request, f'头像更新失败：{str(e)}')
    return redirect('user:profile')

@login_required
def notifications(request):
    """用户通知视图"""
    notifications = request.user.notifications.all().order_by('-created_at')
    unread_count = notifications.filter(is_read=False).count()
    return render(request, 'user/notifications.html', {
        'notifications': notifications,
        'unread_count': unread_count
    })

@login_required
def mark_notification_read(request, notification_id):
    """标记通知为已读"""
    try:
        notification = request.user.notifications.get(id=notification_id)
        notification.is_read = True
        notification.save()
        messages.success(request, '通知已标记为已读')
    except Exception as e:
        messages.error(request, f'操作失败：{str(e)}')
    return redirect('user:notifications')

@login_required
def mark_all_notifications_read(request):
    """标记所有通知为已读"""
    try:
        request.user.notifications.filter(is_read=False).update(is_read=True)
        messages.success(request, '所有通知已标记为已读')
    except Exception as e:
        messages.error(request, f'操作失败：{str(e)}')
    return redirect('user:notifications')

@login_required
def resend_verification(request):
    """重发验证邮件"""
    try:
        if not request.user.userprofile.email_verified:
            # 生成验证令牌
            token = default_token_generator.make_token(request.user)
            uid = urlsafe_base64_encode(force_bytes(request.user.pk))
            verification_url = request.build_absolute_uri(
                reverse('user:verify_email', kwargs={'uidb64': uid, 'token': token})
            )
            
            # 发送验证邮件
            subject = '验证您的邮箱地址'
            message = f'''
            您好 {request.user.username}，

            请点击以下链接验证您的邮箱地址：
            {verification_url}

            如果这不是您的操作，请忽略此邮件。

            祝好，
            福祉网站团队
            '''
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [request.user.email],
                fail_silently=False,
            )
            messages.success(request, '验证邮件已发送，请查收您的邮箱。')
        else:
            messages.info(request, '您的邮箱已经验证过了。')
    except Exception as e:
        messages.error(request, f'发送验证邮件失败：{str(e)}')
    
    return redirect('user:profile')

@login_required
def verify_email(request, uidb64, token):
    """验证邮箱"""
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
        
        if user and default_token_generator.check_token(user, token):
            user.userprofile.email_verified = True
            user.userprofile.save()
            messages.success(request, '邮箱验证成功！')
        else:
            messages.error(request, '验证链接无效或已过期。')
    except (TypeError, ValueError, OverflowError, User.DoesNotExist) as e:
        messages.error(request, f'验证失败：{str(e)}')
    
    return redirect('user:profile')

@login_required
def verify_identity(request):
    """身份验证视图"""
    if request.method == 'POST':
        # 获取表单数据
        real_name = request.POST.get('real_name')
        id_number = request.POST.get('id_number')
        id_photo_front = request.FILES.get('id_photo_front')
        id_photo_back = request.FILES.get('id_photo_back')
        
        try:
            profile = request.user.userprofile
            
            # 更新用户资料
            profile.real_name = real_name
            profile.id_number = id_number
            
            # 保存证件照片
            if id_photo_front:
                profile.id_photo_front = id_photo_front
            if id_photo_back:
                profile.id_photo_back = id_photo_back
                
            # 将验证状态设置为待审核
            profile.identity_status = 'pending'
            profile.save()
            
            messages.success(request, '身份信息已提交，请等待审核。')
            return redirect('user:profile')
            
        except Exception as e:
            messages.error(request, f'提交失败：{str(e)}')
            
    return render(request, 'user/verify_identity.html')

@login_required
def health_info(request):
    """健康信息视图"""
    # 获取或创建健康信息
    health_info, created = HealthInfo.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        try:
            # 更新健康信息
            health_info.height = request.POST.get('height') or None
            health_info.weight = request.POST.get('weight') or None
            health_info.blood_type = request.POST.get('blood_type', 'unknown')
            health_info.allergies = request.POST.get('allergies', '')
            health_info.medical_history = request.POST.get('medical_history', '')
            health_info.medications = request.POST.get('medications', '')
            health_info.emergency_medical_info = request.POST.get('emergency_medical_info', '')
            health_info.save()
            
            messages.success(request, '健康信息更新成功！')
            return redirect('user:health_info')
            
        except Exception as e:
            messages.error(request, f'更新失败：{str(e)}')
    
    return render(request, 'user/health_info.html', {'health_info': health_info})

@login_required
def emergency_contacts(request):
    """紧急联系人列表视图"""
    contacts = request.user.emergency_contacts.all()
    return render(request, 'user/emergency_contacts.html', {'contacts': contacts})

@login_required
def add_emergency_contact(request):
    """添加紧急联系人视图"""
    if request.method == 'POST':
        try:
            # 获取表单数据
            name = request.POST.get('name')
            relationship = request.POST.get('relationship')
            phone = request.POST.get('phone')
            address = request.POST.get('address', '')
            note = request.POST.get('note', '')
            
            # 创建紧急联系人
            EmergencyContact.objects.create(
                user=request.user,
                name=name,
                relationship=relationship,
                phone=phone,
                address=address,
                note=note
            )
            
            messages.success(request, '紧急联系人添加成功！')
            return redirect('user:emergency_contacts')
            
        except Exception as e:
            messages.error(request, f'添加失败：{str(e)}')
            
    return render(request, 'user/add_emergency_contact.html')

@login_required
def edit_emergency_contact(request, contact_id):
    """编辑紧急联系人视图"""
    try:
        contact = EmergencyContact.objects.get(id=contact_id, user=request.user)
    except EmergencyContact.DoesNotExist:
        messages.error(request, '紧急联系人不存在！')
        return redirect('user:emergency_contacts')
        
    if request.method == 'POST':
        try:
            # 更新联系人信息
            contact.name = request.POST.get('name')
            contact.relationship = request.POST.get('relationship')
            contact.phone = request.POST.get('phone')
            contact.address = request.POST.get('address', '')
            contact.note = request.POST.get('note', '')
            contact.save()
            
            messages.success(request, '紧急联系人更新成功！')
            return redirect('user:emergency_contacts')
            
        except Exception as e:
            messages.error(request, f'更新失败：{str(e)}')
            
    return render(request, 'user/edit_emergency_contact.html', {'contact': contact})

@login_required
def delete_emergency_contact(request, contact_id):
    """删除紧急联系人视图"""
    try:
        contact = EmergencyContact.objects.get(id=contact_id, user=request.user)
        contact.delete()
        messages.success(request, '紧急联系人删除成功！')
    except EmergencyContact.DoesNotExist:
        messages.error(request, '紧急联系人不存在！')
    except Exception as e:
        messages.error(request, f'删除失败：{str(e)}')
        
    return redirect('user:emergency_contacts')

@login_required
def service_history(request):
    """服务历史记录视图"""
    # 获取用户的服务预约记录
    from serviceApp.models import ServiceAppointment
    
    # 获取所有状态的服务预约
    service_appointments = ServiceAppointment.objects.filter(
        user=request.user
    ).select_related('service').order_by('-created_time')
    
    # 按状态分类
    pending_services = service_appointments.filter(status='pending')
    ongoing_services = service_appointments.filter(status='confirmed')
    completed_services = service_appointments.filter(status='completed')
    cancelled_services = service_appointments.filter(status='cancelled')
    
    context = {
        'pending_services': pending_services,
        'ongoing_services': ongoing_services,
        'completed_services': completed_services,
        'cancelled_services': cancelled_services,
    }
    
    return render(request, 'user/service_history.html', context)

@login_required
def volunteer_history(request):
    """志愿服务历史记录视图"""
    # 获取用户的志愿服务申请记录
    from volunteerApp.models import VolunteerApplication
    
    # 获取所有状态的志愿服务申请
    volunteer_applications = VolunteerApplication.objects.filter(
        user=request.user
    ).select_related('activity').order_by('-created_time')
    
    # 按状态分类
    pending_activities = volunteer_applications.filter(status='pending')
    ongoing_activities = volunteer_applications.filter(status='ongoing')
    completed_activities = volunteer_applications.filter(status='completed')
    cancelled_activities = volunteer_applications.filter(status='cancelled')
    
    context = {
        'pending_activities': pending_activities,
        'ongoing_activities': ongoing_activities,
        'completed_activities': completed_activities,
        'cancelled_activities': cancelled_activities,
    }
    
    return render(request, 'user/volunteer_history.html', context)
