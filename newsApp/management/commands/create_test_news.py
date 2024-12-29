from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from newsApp.models import NewsCategory, News
from django.utils import timezone
import random

class Command(BaseCommand):
    help = '创建测试新闻数据'

    def handle(self, *args, **kwargs):
        # 确保有管理员用户
        admin_user, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'is_staff': True,
                'is_superuser': True,
                'email': 'admin@example.com'
            }
        )
        if created:
            admin_user.set_password('admin123')
            admin_user.save()

        # 创建新闻分类
        categories = [
            {'name': '政策动态', 'description': '最新的养老政策和行业动态'},
            {'name': '健康资讯', 'description': '养老健康知识和医疗信息'},
            {'name': '活动公告', 'description': '各类养老活动和公告信息'},
            {'name': '服务信息', 'description': '养老服务相关信息'},
        ]

        for cat_data in categories:
            category, created = NewsCategory.objects.get_or_create(
                name=cat_data['name'],
                defaults={'description': cat_data['description']}
            )
            if created:
                self.stdout.write(f'Created category: {category.name}')

        # 创建新闻
        titles = [
            '养老服务质量提升工程全面启动',
            '智慧养老新模式：科技赋能幸福晚年',
            '社区养老服务中心建设指南发布',
            '老年人营养膳食指南更新',
            '养老机构服务标准体系完善',
            '老年人心理健康关爱计划实施',
            '医养结合示范项目成效显著',
            '老年教育资源开放计划启动',
            '养老服务人才培养工程开展',
            '适老化改造补贴政策出台',
        ]

        for i, title in enumerate(titles):
            category = NewsCategory.objects.order_by('?').first()
            news, created = News.objects.get_or_create(
                title=title,
                defaults={
                    'author': admin_user,
                    'category': category,
                    'summary': f'{title}的详细介绍和分析报告。',
                    'content': f'<h2>{title}</h2><p>这是一篇关于{title}的详细新闻报道。包含了相关政策解读、实施方案、效果分析等内容。</p>',
                    'status': 'published',
                    'views': random.randint(100, 1000),
                    'is_pinned': i < 2,  # 前两条新闻置顶
                }
            )
            if created:
                self.stdout.write(f'Created news: {news.title}')

        self.stdout.write(self.style.SUCCESS('Successfully created test news data'))
