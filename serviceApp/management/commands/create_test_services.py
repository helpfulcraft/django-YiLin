from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from serviceApp.models import ServiceCategory, Service
from django.utils import timezone
from decimal import Decimal

class Command(BaseCommand):
    help = '创建测试服务数据'

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

        # 创建服务类别
        categories = [
            {
                'name': '生活照料',
                'description': '提供日常生活照料服务，包括个人卫生、饮食起居等',
                'icon': 'bi-heart-fill',
                'index': 1
            },
            {
                'name': '医疗护理',
                'description': '提供专业的医疗护理服务，包括康复训练、用药指导等',
                'icon': 'bi-hospital',
                'index': 2
            },
            {
                'name': '精神慰藉',
                'description': '提供心理咨询、情感陪伴等精神关怀服务',
                'icon': 'bi-emoji-smile',
                'index': 3
            },
            {
                'name': '文娱活动',
                'description': '组织各类文化娱乐活动，丰富老年人精神生活',
                'icon': 'bi-music-note',
                'index': 4
            }
        ]

        for cat_data in categories:
            category, created = ServiceCategory.objects.get_or_create(
                name=cat_data['name'],
                defaults={
                    'description': cat_data['description'],
                    'icon': cat_data['icon'],
                    'index': cat_data['index']
                }
            )
            if created:
                self.stdout.write(f'Created category: {category.name}')

        # 创建服务项目
        services = [
            {
                'category': '生活照料',
                'name': '居家照护服务',
                'short_description': '提供专业的居家照护服务，包括生活起居照料、卫生清洁等',
                'content': '''
                    <h3>服务内容</h3>
                    <ul>
                        <li>生活起居照料</li>
                        <li>个人卫生护理</li>
                        <li>房间卫生清洁</li>
                        <li>膳食营养搭配</li>
                    </ul>
                    <h3>服务标准</h3>
                    <p>由专业护理人员提供一对一服务，确保服务质量和安全。</p>
                ''',
                'price': Decimal('100.00'),
                'duration': '2小时',
                'is_featured': True
            },
            {
                'category': '医疗护理',
                'name': '康复理疗服务',
                'short_description': '提供专业的康复理疗服务，帮助恢复身体机能',
                'content': '''
                    <h3>服务内容</h3>
                    <ul>
                        <li>康复训练指导</li>
                        <li>物理治疗</li>
                        <li>功能评估</li>
                        <li>康复计划制定</li>
                    </ul>
                    <h3>服务标准</h3>
                    <p>由专业康复师提供一对一服务，制定个性化康复方案。</p>
                ''',
                'price': Decimal('150.00'),
                'duration': '1小时',
                'is_featured': True
            },
            {
                'category': '精神慰藉',
                'name': '心理咨询服务',
                'short_description': '提供专业的心理咨询服务，帮助缓解心理压力',
                'content': '''
                    <h3>服务内容</h3>
                    <ul>
                        <li>心理评估</li>
                        <li>情绪疏导</li>
                        <li>压力管理</li>
                        <li>家庭关系协调</li>
                    </ul>
                    <h3>服务标准</h3>
                    <p>由专业心理咨询师提供一对一服务，保证隐私安全。</p>
                ''',
                'price': Decimal('200.00'),
                'duration': '1小时',
                'is_featured': False
            },
            {
                'category': '文娱活动',
                'name': '兴趣班课程',
                'short_description': '开设书法、绘画、太极等兴趣班课程',
                'content': '''
                    <h3>课程内容</h3>
                    <ul>
                        <li>书法课程</li>
                        <li>国画课程</li>
                        <li>太极拳课程</li>
                        <li>音乐欣赏课程</li>
                    </ul>
                    <h3>课程标准</h3>
                    <p>由专业老师授课，小班教学，因材施教。</p>
                ''',
                'price': Decimal('50.00'),
                'duration': '2小时',
                'is_featured': False
            }
        ]

        for service_data in services:
            category = ServiceCategory.objects.get(name=service_data['category'])
            service, created = Service.objects.get_or_create(
                name=service_data['name'],
                defaults={
                    'category': category,
                    'short_description': service_data['short_description'],
                    'content': service_data['content'],
                    'price': service_data['price'],
                    'duration': service_data['duration'],
                    'is_featured': service_data['is_featured'],
                    'status': 'active'
                }
            )
            if created:
                self.stdout.write(f'Created service: {service.name}')

        self.stdout.write(self.style.SUCCESS('Successfully created test service data'))
