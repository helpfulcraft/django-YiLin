from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.

class UserProfile(models.Model):
    """用户信息模型"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='用户')
    avatar = models.ImageField('头像', upload_to='avatars/', blank=True)
    phone = models.CharField('手机号', max_length=11, blank=True)
    address = models.CharField('地址', max_length=200, blank=True)
    created_time = models.DateTimeField('创建时间', default=timezone.now)
    updated_time = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.user.username
