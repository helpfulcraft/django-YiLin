from django.db import models
from django.urls import reverse
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils import timezone
from django.contrib.auth.models import User

class ServiceCategory(models.Model):
    """服务类别"""
    name = models.CharField('类别名称', max_length=100)
    description = models.TextField('类别描述')
    icon = models.CharField('图标类名', max_length=50, help_text='Font Awesome图标类名')
    index = models.IntegerField('排序', default=0)

    class Meta:
        verbose_name = '服务类别'
        verbose_name_plural = verbose_name
        ordering = ['index']

    def __str__(self):
        return self.name

class Service(models.Model):
    """服务项目"""
    STATUS_CHOICES = (
        ('active', '正常'),
        ('suspended', '暂停'),
        ('discontinued', '停止'),
    )
    
    category = models.ForeignKey(ServiceCategory, verbose_name='服务类别', on_delete=models.CASCADE)
    name = models.CharField('服务名称', max_length=200)
    image = models.ImageField('服务图片', upload_to='services/')
    short_description = models.TextField('简短描述')
    content = RichTextUploadingField('服务详情')
    price = models.DecimalField('价格', max_digits=10, decimal_places=2, help_text='元/次')
    duration = models.CharField('服务时长', max_length=50, help_text='如：2小时')
    is_featured = models.BooleanField('是否特色服务', default=False)
    status = models.CharField('服务状态', max_length=20, choices=STATUS_CHOICES, default='active')
    created_time = models.DateTimeField('创建时间', default=timezone.now)
    updated_time = models.DateTimeField('更新时间', auto_now=True, null=True, blank=True)

    class Meta:
        verbose_name = '服务项目'
        verbose_name_plural = verbose_name
        ordering = ['-created_time']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('service_detail', args=[str(self.id)])

    @property
    def is_active(self):
        return self.status == 'active'

class ServiceAppointment(models.Model):
    """服务预约"""
    STATUS_CHOICES = (
        ('pending', '待确认'),
        ('confirmed', '已确认'),
        ('completed', '已完成'),
        ('cancelled', '已取消'),
    )
    
    service = models.ForeignKey(Service, verbose_name='服务项目', on_delete=models.CASCADE)
    user = models.ForeignKey(User, verbose_name='预约用户', on_delete=models.CASCADE)
    appointment_time = models.DateTimeField('预约时间', default=timezone.now)
    status = models.CharField('预约状态', max_length=20, choices=STATUS_CHOICES, default='pending')
    note = models.TextField('备注', blank=True)
    created_time = models.DateTimeField('创建时间', default=timezone.now)
    updated_time = models.DateTimeField('更新时间', auto_now=True, null=True, blank=True)

    class Meta:
        verbose_name = '服务预约'
        verbose_name_plural = verbose_name
        ordering = ['-appointment_time']

    def __str__(self):
        return f'{self.user.username} - {self.service.name}'

class ServiceReview(models.Model):
    """服务评价"""
    service = models.ForeignKey(Service, verbose_name='服务项目', on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, verbose_name='评价用户', on_delete=models.CASCADE)
    rating = models.IntegerField('评分', choices=[(i, i) for i in range(1, 6)])
    content = models.TextField('评价内容')
    created_at = models.DateTimeField('创建时间', default=timezone.now)
    updated_time = models.DateTimeField('更新时间', auto_now=True, null=True, blank=True)

    class Meta:
        verbose_name = '服务评价'
        verbose_name_plural = verbose_name
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.user.username} - {self.service.name} - {self.rating}星'
