from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.

class Activity(models.Model):
    """志愿活动模型"""
    title = models.CharField('活动标题', max_length=100)
    description = models.TextField('活动描述')
    date = models.DateField('活动日期')
    location = models.CharField('活动地点', max_length=100)
    volunteers_needed = models.IntegerField('所需志愿者数量')
    created_at = models.DateTimeField('创建时间', default=timezone.now)

    class Meta:
        verbose_name = '志愿活动'
        verbose_name_plural = verbose_name
        ordering = ['-date']

    def __str__(self):
        return self.title

class Application(models.Model):
    """志愿申请模型"""
    STATUS_CHOICES = [
        ('pending', '待审核'),
        ('approved', '已通过'),
        ('rejected', '已拒绝')
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='申请人')
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE, verbose_name='活动')
    status = models.CharField('状态', max_length=20, choices=STATUS_CHOICES, default='pending')
    apply_reason = models.TextField('申请理由')
    created_at = models.DateTimeField('申请时间', default=timezone.now)

    class Meta:
        verbose_name = '志愿申请'
        verbose_name_plural = verbose_name
        ordering = ['-created_at']
        unique_together = ['user', 'activity']

    def __str__(self):
        return f'{self.user.username} - {self.activity.title}'
