from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from django.core.validators import MinValueValidator
from django.utils import timezone

class ActivityCategory(models.Model):
    """活动分类"""
    name = models.CharField('分类名称', max_length=50)
    description = models.TextField('分类描述', blank=True)
    order = models.IntegerField('排序', default=0)
    
    class Meta:
        verbose_name = '活动分类'
        verbose_name_plural = verbose_name
        ordering = ['name']
    
    def __str__(self):
        return self.name

class VolunteerActivity(models.Model):
    """志愿活动模型"""
    STATUS_CHOICES = [
        ('draft', '草稿'),
        ('published', '已发布'),
        ('closed', '已结束'),
    ]
    
    title = models.CharField('活动标题', max_length=200)
    description = RichTextField('活动描述')
    category = models.ForeignKey(ActivityCategory, on_delete=models.SET_NULL, null=True, verbose_name='活动分类')
    location = models.CharField('活动地点', max_length=200)
    start_time = models.DateTimeField('开始时间')
    end_time = models.DateTimeField('结束时间')
    required_volunteers = models.IntegerField('所需志愿者数量', validators=[MinValueValidator(1)])
    current_volunteers = models.IntegerField('当前志愿者数量', default=0)
    status = models.CharField('状态', max_length=10, choices=STATUS_CHOICES, default='draft')
    created_time = models.DateTimeField('创建时间', default=timezone.now)
    updated_time = models.DateTimeField('更新时间', auto_now=True)
    image = models.ImageField('活动图片', upload_to='volunteer/activities/', blank=True, null=True)
    organizer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='organized_activities', verbose_name='组织者', null=True, blank=True)

    class Meta:
        verbose_name = '志愿活动'
        verbose_name_plural = verbose_name
        ordering = ['-created_time']

    def __str__(self):
        return self.title

    def is_active(self):
        """活动是否进行中"""
        now = timezone.now()
        return self.start_time <= now <= self.end_time

    def is_full(self):
        """活动是否已满"""
        return self.current_volunteers >= self.required_volunteers

    def save(self, *args, **kwargs):
        # Automatically update current_volunteers based on approved applications
        if self.pk:
            self.current_volunteers = self.applications.filter(status='approved').count()
        super().save(*args, **kwargs)

class VolunteerApplication(models.Model):
    """志愿者申请模型"""
    STATUS_CHOICES = [
        ('pending', '待审核'),
        ('approved', '已通过'),
        ('rejected', '已拒绝'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='用户')
    activity = models.ForeignKey(VolunteerActivity, on_delete=models.CASCADE, related_name='applications', verbose_name='活动')
    status = models.CharField('申请状态', max_length=10, choices=STATUS_CHOICES, default='pending')
    message = models.TextField('申请留言', blank=True)
    created_time = models.DateTimeField('申请时间', default=timezone.now)
    updated_time = models.DateTimeField('更新时间', auto_now=True)
    
    class Meta:
        verbose_name = '志愿申请'
        verbose_name_plural = verbose_name
        ordering = ['-created_time']
        unique_together = ['user', 'activity']

    def __str__(self):
        return f'{self.user.username} - {self.activity.title}'

class ActivityComment(models.Model):
    """活动评论模型"""
    activity = models.ForeignKey(VolunteerActivity, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activity_comments')
    content = models.TextField('评论内容')
    created_time = models.DateTimeField('创建时间', auto_now_add=True)
    updated_time = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        verbose_name = '活动评论'
        verbose_name_plural = verbose_name
        ordering = ['-created_time']

    def __str__(self):
        return f'{self.user.username}对{self.activity.title}的评论'

class VolunteerProfile(models.Model):
    """志愿者档案模型"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='用户')
    total_hours = models.FloatField('志愿时长', default=0)
    skill_tags = models.CharField('技能标签', max_length=200, blank=True)
    introduction = models.TextField('个人简介', blank=True)
    created_time = models.DateTimeField('创建时间', auto_now_add=True)
    updated_time = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        verbose_name = '志愿者档案'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f'{self.user.username}的志愿者档案'
