# Generated by Django 4.2 on 2024-12-28 05:00

import ckeditor.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='标题')),
                ('cover', models.ImageField(blank=True, upload_to='news/covers/%Y/%m/', verbose_name='封面图片')),
                ('summary', models.TextField(verbose_name='摘要')),
                ('content', ckeditor.fields.RichTextField(verbose_name='内容')),
                ('status', models.CharField(choices=[('draft', '草稿'), ('published', '已发布')], default='draft', max_length=10, verbose_name='状态')),
                ('views', models.PositiveIntegerField(default=0, verbose_name='浏览量')),
                ('is_pinned', models.BooleanField(default=False, verbose_name='置顶')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('updated_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='news', to=settings.AUTH_USER_MODEL, verbose_name='作者')),
            ],
            options={
                'verbose_name': '新闻',
                'verbose_name_plural': '新闻',
                'ordering': ['-is_pinned', '-created_time'],
            },
        ),
        migrations.CreateModel(
            name='NewsCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='分类名称')),
                ('description', models.TextField(blank=True, verbose_name='描述')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
            ],
            options={
                'verbose_name': '新闻分类',
                'verbose_name_plural': '新闻分类',
                'ordering': ['-created_time'],
            },
        ),
        migrations.CreateModel(
            name='NewsComment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(verbose_name='评论内容')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='评论时间')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='news_comments', to=settings.AUTH_USER_MODEL, verbose_name='评论者')),
                ('news', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='newsApp.news', verbose_name='新闻')),
            ],
            options={
                'verbose_name': '新闻评论',
                'verbose_name_plural': '新闻评论',
                'ordering': ['-created_time'],
            },
        ),
        migrations.AddField(
            model_name='news',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='news', to='newsApp.newscategory', verbose_name='分类'),
        ),
    ]
