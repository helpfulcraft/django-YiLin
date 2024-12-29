from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.conf import settings
from ckeditor.fields import RichTextField

class NewsCategory(models.Model):
    """新闻分类"""
    name = models.CharField('分类名称', max_length=100)
    description = models.TextField('描述', blank=True)
    created_time = models.DateTimeField('创建时间', auto_now_add=True)
    
    class Meta:
        verbose_name = '新闻分类'
        verbose_name_plural = verbose_name
        ordering = ['-created_time']
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('news:list') + f'?category={self.pk}'

class News(models.Model):
    """新闻"""
    STATUS_CHOICES = (
        ('draft', '草稿'),
        ('published', '已发布'),
    )
    
    title = models.CharField('标题', max_length=200)
    author = models.ForeignKey(
        User, 
        verbose_name='作者',
        on_delete=models.CASCADE,
        related_name='news'
    )
    category = models.ForeignKey(
        NewsCategory,
        verbose_name='分类',
        on_delete=models.CASCADE,
        related_name='news'
    )
    cover = models.ImageField('封面图片', upload_to='news/covers/%Y/%m/', blank=True)
    summary = models.TextField('摘要')
    content = RichTextField('内容')
    status = models.CharField('状态', max_length=10, choices=STATUS_CHOICES, default='draft')
    views = models.PositiveIntegerField('浏览量', default=0)
    is_pinned = models.BooleanField('置顶', default=False)
    created_time = models.DateTimeField('创建时间', auto_now_add=True)
    updated_time = models.DateTimeField('更新时间', auto_now=True)
    
    class Meta:
        verbose_name = '新闻'
        verbose_name_plural = verbose_name
        ordering = ['-is_pinned', '-created_time']
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('news:detail', kwargs={'pk': self.pk})
    
    def get_related_news(self):
        """获取相关新闻"""
        return News.objects.filter(
            category=self.category,
            status='published'
        ).exclude(pk=self.pk)[:5]

class NewsComment(models.Model):
    """新闻评论"""
    news = models.ForeignKey(
        News,
        verbose_name='新闻',
        on_delete=models.CASCADE,
        related_name='comments'
    )
    author = models.ForeignKey(
        User,
        verbose_name='评论者',
        on_delete=models.CASCADE,
        related_name='news_comments'
    )
    content = models.TextField('评论内容')
    created_time = models.DateTimeField('评论时间', auto_now_add=True)
    
    class Meta:
        verbose_name = '新闻评论'
        verbose_name_plural = verbose_name
        ordering = ['-created_time']
    
    def __str__(self):
        return f'{self.author.username} 评论了 {self.news.title}'
