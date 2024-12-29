from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

class UserProfile(models.Model):
    """用户资料模型"""
    IDENTITY_STATUS_CHOICES = [
        ('unverified', '未验证'),
        ('pending', '审核中'),
        ('verified', '已验证'),
        ('rejected', '已拒绝'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField('头像', upload_to='avatars/%Y/%m/', default='avatars/default.png', null=True, blank=True)
    bio = models.TextField('个人简介', max_length=500, blank=True)
    email_verified = models.BooleanField(default=False)
    
    # 身份验证字段
    real_name = models.CharField(max_length=50, blank=True)
    id_number = models.CharField(max_length=18, blank=True)
    id_photo_front = models.ImageField(upload_to='id_photos/', null=True, blank=True)
    id_photo_back = models.ImageField(upload_to='id_photos/', null=True, blank=True)
    identity_status = models.CharField(
        max_length=20,
        choices=IDENTITY_STATUS_CHOICES,
        default='unverified'
    )
    created_time = models.DateTimeField('创建时间', default=timezone.now)
    updated_time = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        verbose_name = '用户资料'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """创建用户时自动创建用户资料"""
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """保存用户时自动保存用户资料"""
    instance.userprofile.save()

class Notification(models.Model):
    """用户通知模型"""
    NOTIFICATION_TYPES = (
        ('info', '信息'),
        ('success', '成功'),
        ('warning', '警告'),
        ('error', '错误'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=100)
    message = models.TextField()
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES, default='info')
    url = models.CharField(max_length=200, blank=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f'{self.user.username}的通知：{self.title}'

class EmergencyContact(models.Model):
    """紧急联系人模型"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='emergency_contacts')
    name = models.CharField('姓名', max_length=50)
    relationship = models.CharField('关系', max_length=50)
    phone = models.CharField('电话', max_length=20)
    address = models.CharField('地址', max_length=200, blank=True)
    note = models.TextField('备注', max_length=500, blank=True)
    created_time = models.DateTimeField('创建时间', default=timezone.now)
    updated_time = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        verbose_name = '紧急联系人'
        verbose_name_plural = verbose_name
        ordering = ['-created_time']

    def __str__(self):
        return f"{self.user.username}的紧急联系人：{self.name}"

class HealthInfo(models.Model):
    """健康信息模型"""
    BLOOD_TYPE_CHOICES = [
        ('A', 'A型'),
        ('B', 'B型'),
        ('O', 'O型'),
        ('AB', 'AB型'),
        ('unknown', '未知'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='health_info')
    height = models.DecimalField('身高(cm)', max_digits=5, decimal_places=1, null=True, blank=True)
    weight = models.DecimalField('体重(kg)', max_digits=5, decimal_places=1, null=True, blank=True)
    blood_type = models.CharField('血型', max_length=10, choices=BLOOD_TYPE_CHOICES, default='unknown')
    allergies = models.TextField('过敏史', blank=True)
    medical_history = models.TextField('既往病史', blank=True)
    medications = models.TextField('当前用药', blank=True)
    emergency_medical_info = models.TextField('紧急医疗信息', blank=True)
    created_time = models.DateTimeField('创建时间', default=timezone.now)
    updated_time = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        verbose_name = '健康信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.user.username}的健康信息"
