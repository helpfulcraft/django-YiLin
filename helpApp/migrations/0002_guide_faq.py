# Generated by Django 4.2 on 2024-12-28 11:49

import ckeditor.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('helpApp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Guide',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='标题')),
                ('content', ckeditor.fields.RichTextField(verbose_name='内容')),
                ('order', models.IntegerField(default=0, verbose_name='排序')),
                ('is_published', models.BooleanField(default=True, verbose_name='是否发布')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('updated_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='helpApp.helpcategory', verbose_name='分类')),
            ],
            options={
                'verbose_name': '使用指南',
                'verbose_name_plural': '使用指南',
                'ordering': ['order', '-created_time'],
            },
        ),
        migrations.CreateModel(
            name='FAQ',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(max_length=200, verbose_name='问题')),
                ('answer', ckeditor.fields.RichTextField(verbose_name='答案')),
                ('order', models.IntegerField(default=0, verbose_name='排序')),
                ('is_published', models.BooleanField(default=True, verbose_name='是否发布')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('updated_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='helpApp.helpcategory', verbose_name='分类')),
            ],
            options={
                'verbose_name': '常见问题',
                'verbose_name_plural': '常见问题',
                'ordering': ['order', '-created_time'],
            },
        ),
    ]
