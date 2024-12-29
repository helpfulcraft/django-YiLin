from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField

# Create your models here.

class HelpCategory(models.Model):
    """帮助分类"""
    name = models.CharField('分类名称', max_length=100)
    description = models.TextField('分类描述', blank=True)
    icon = models.CharField('图标类名', max_length=50, help_text='Font Awesome图标类名')
    order = models.IntegerField('排序', default=0)
    created_time = models.DateTimeField('创建时间', auto_now_add=True)
    updated_time = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        verbose_name = '帮助分类'
        verbose_name_plural = verbose_name
        ordering = ['order', 'created_time']

    def __str__(self):
        return self.name

class HelpArticle(models.Model):
    """帮助文章"""
    category = models.ForeignKey(HelpCategory, on_delete=models.CASCADE, verbose_name='分类')
    title = models.CharField('标题', max_length=200)
    content = RichTextField('内容')
    views = models.PositiveIntegerField('浏览次数', default=0)
    is_published = models.BooleanField('是否发布', default=True)
    created_time = models.DateTimeField('创建时间', auto_now_add=True)
    updated_time = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        verbose_name = '帮助文章'
        verbose_name_plural = verbose_name
        ordering = ['-created_time']

    def __str__(self):
        return self.title

class FAQ(models.Model):
    """常见问题"""
    category = models.ForeignKey(HelpCategory, on_delete=models.CASCADE, verbose_name='分类')
    question = models.CharField('问题', max_length=200)
    answer = RichTextField('答案')
    order = models.IntegerField('排序', default=0)
    is_published = models.BooleanField('是否发布', default=True)
    created_time = models.DateTimeField('创建时间', auto_now_add=True)
    updated_time = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        verbose_name = '常见问题'
        verbose_name_plural = verbose_name
        ordering = ['order', '-created_time']

    def __str__(self):
        return self.question

class Guide(models.Model):
    """使用指南"""
    title = models.CharField('标题', max_length=200)
    content = RichTextField('内容')
    category = models.ForeignKey(HelpCategory, on_delete=models.CASCADE, verbose_name='分类')
    order = models.IntegerField('排序', default=0)
    is_published = models.BooleanField('是否发布', default=True)
    created_time = models.DateTimeField('创建时间', auto_now_add=True)
    updated_time = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        verbose_name = '使用指南'
        verbose_name_plural = verbose_name
        ordering = ['order', '-created_time']

    def __str__(self):
        return self.title

class Feedback(models.Model):
    """反馈"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='用户')
    title = models.CharField('标题', max_length=200)
    content = models.TextField('内容')
    status = models.CharField('状态', max_length=20, choices=[
        ('pending', '待处理'),
        ('processing', '处理中'),
        ('resolved', '已解决'),
        ('closed', '已关闭'),
    ], default='pending')
    reply = models.TextField('回复', blank=True)
    created_time = models.DateTimeField('创建时间', auto_now_add=True)
    updated_time = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        verbose_name = '反馈'
        verbose_name_plural = verbose_name
        ordering = ['-created_time']

    def __str__(self):
        return self.title

class OnlineConsultation(models.Model):
    """在线咨询"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='用户')
    category = models.CharField('咨询类型', max_length=50, choices=[
        ('service', '服务咨询'),
        ('volunteer', '志愿服务'),
        ('account', '账号相关'),
        ('other', '其他'),
    ])
    title = models.CharField('标题', max_length=200)
    content = models.TextField('内容')
    status = models.CharField('状态', max_length=20, choices=[
        ('pending', '待回复'),
        ('replied', '已回复'),
        ('closed', '已关闭'),
    ], default='pending')
    reply = models.TextField('回复', blank=True)
    created_time = models.DateTimeField('创建时间', auto_now_add=True)
    updated_time = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        verbose_name = '在线咨询'
        verbose_name_plural = verbose_name
        ordering = ['-created_time']

    def __str__(self):
        return self.title
