from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField

class Carousel(models.Model):
    """首页轮播图"""
    title = models.CharField('标题', max_length=100)
    description = models.TextField('描述', blank=True)
    image = models.ImageField('图片', upload_to='carousel/')
    link = models.URLField('链接', blank=True)
    order = models.IntegerField('排序', default=0)
    is_active = models.BooleanField('是否启用', default=True)
    created_time = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        verbose_name = '轮播图'
        verbose_name_plural = verbose_name
        ordering = ['order', '-created_time']

    def __str__(self):
        return self.title

class Activity(models.Model):
    """活动信息"""
    title = models.CharField('标题', max_length=200)
    description = models.TextField('简介', default='暂无简介')
    image = models.ImageField('封面图', upload_to='activities/', blank=True, null=True)
    content = RichTextUploadingField('活动内容')
    start_time = models.DateTimeField('开始时间')
    end_time = models.DateTimeField('结束时间')
    location = models.CharField('活动地点', max_length=200)
    volunteers_needed = models.IntegerField('所需志愿者', default=1)
    volunteers_registered = models.IntegerField('已报名志愿者', default=0)
    is_active = models.BooleanField('是否进行中', default=True)
    is_featured = models.BooleanField('是否推荐', default=False)
    created_time = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        verbose_name = '活动信息'
        verbose_name_plural = verbose_name
        ordering = ['-is_featured', '-start_time']

    def __str__(self):
        return self.title

    @property
    def registration_progress(self):
        """报名进度"""
        if self.volunteers_needed == 0:
            return 100
        return int((self.volunteers_registered / self.volunteers_needed) * 100)

class ServiceHighlight(models.Model):
    """服务亮点"""
    title = models.CharField('标题', max_length=100)
    description = models.TextField('描述', default='')
    icon = models.CharField('图标类名', max_length=50, help_text='Font Awesome图标类名', default='')
    index = models.IntegerField('排序', default=0)
    is_active = models.BooleanField('是否启用', default=True)

    class Meta:
        verbose_name = '服务亮点'
        verbose_name_plural = verbose_name
        ordering = ['index']

    def __str__(self):
        return self.title

class Statistic(models.Model):
    """首页统计数据"""
    title = models.CharField('标题', max_length=100)
    value = models.CharField('数值', max_length=50)
    icon = models.CharField('图标类名', max_length=50, help_text='Font Awesome图标类名', default='')
    index = models.IntegerField('排序', default=0)
    is_active = models.BooleanField('是否启用', default=True)

    class Meta:
        verbose_name = '统计数据'
        verbose_name_plural = verbose_name
        ordering = ['index']

    def __str__(self):
        return self.title
