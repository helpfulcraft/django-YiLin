from django.db import models
from django.utils import timezone

# Create your models here.

class Banner(models.Model):
    """首页轮播图模型"""
    title = models.CharField('标题', max_length=200)
    subtitle = models.CharField('副标题', max_length=200, blank=True)
    description = models.TextField('描述', blank=True)
    image = models.ImageField('图片', upload_to='banners/')
    url = models.URLField('链接', blank=True)
    order = models.IntegerField('排序', default=0)
    is_active = models.BooleanField('是否启用', default=True)
    start_time = models.DateTimeField('开始时间', default=timezone.now)
    end_time = models.DateTimeField('结束时间', default=timezone.now)
    created_time = models.DateTimeField('创建时间', auto_now_add=True)
    updated_time = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        verbose_name = '轮播图'
        verbose_name_plural = verbose_name
        ordering = ['order', '-created_time']

    def __str__(self):
        return self.title

    def is_valid(self):
        """检查轮播图是否在有效期内"""
        now = timezone.now()
        return self.is_active and self.start_time <= now <= self.end_time

class Statistics(models.Model):
    """网站统计数据模型"""
    title = models.CharField('标题', max_length=100)
    value = models.IntegerField('数值')
    icon = models.CharField('图标', max_length=50)
    order = models.IntegerField('排序', default=0)
    is_active = models.BooleanField('是否启用', default=True)
    created_time = models.DateTimeField('创建时间', auto_now_add=True)
    updated_time = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        verbose_name = '统计数据'
        verbose_name_plural = verbose_name
        ordering = ['order']

    def __str__(self):
        return self.title
