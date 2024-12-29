from django.core.management.base import BaseCommand
from django.utils import timezone
from homeApp.models import Banner, ServiceHighlight, Statistic, Activity
from newsApp.models import News
from serviceApp.models import Service

class Command(BaseCommand):
    help = '填充首页所需的示例数据'

    def handle(self, *args, **options):
        # 创建轮播图
        banners_data = [
            {
                'title': '志愿服务，温暖人心',
                'description': '加入我们，一起传递爱心和温暖',
                'image': 'banners/banner1.jpg',
                'index': 1,
            },
            {
                'title': '爱心助老，情暖夕阳',
                'description': '为老年人提供关爱和服务',
                'image': 'banners/banner2.jpg',
                'index': 2,
            },
            {
                'title': '关爱儿童，守护未来',
                'description': '为儿童提供教育和关爱',
                'image': 'banners/banner3.jpg',
                'index': 3,
            },
        ]

        self.stdout.write('创建轮播图...')
        for data in banners_data:
            Banner.objects.get_or_create(
                title=data['title'],
                defaults={
                    'description': data['description'],
                    'image': data['image'],
                    'index': data['index'],
                }
            )

        # 创建服务特色
        highlights_data = [
            {
                'title': '专业服务',
                'description': '我们的志愿者都经过专业培训',
                'icon': 'fas fa-user-md',
                'index': 1,
            },
            {
                'title': '全天候支持',
                'description': '24小时随时待命，为您提供帮助',
                'icon': 'fas fa-clock',
                'index': 2,
            },
            {
                'title': '无偿服务',
                'description': '所有服务均为公益性质，完全免费',
                'icon': 'fas fa-heart',
                'index': 3,
            },
        ]

        self.stdout.write('创建服务特色...')
        for data in highlights_data:
            ServiceHighlight.objects.get_or_create(
                title=data['title'],
                defaults={
                    'description': data['description'],
                    'icon': data['icon'],
                    'index': data['index'],
                }
            )

        # 创建统计数据
        statistics_data = [
            {
                'title': '注册志愿者',
                'value': '1200+',
                'icon': 'fas fa-users',
                'index': 1,
            },
            {
                'title': '进行中的活动',
                'value': '50+',
                'icon': 'fas fa-calendar-alt',
                'index': 2,
            },
            {
                'title': '合作机构',
                'value': '100+',
                'icon': 'fas fa-handshake',
                'index': 3,
            },
            {
                'title': '服务时长',
                'value': '5000+',
                'icon': 'fas fa-clock',
                'index': 4,
            },
        ]

        self.stdout.write('创建统计数据...')
        for data in statistics_data:
            Statistic.objects.get_or_create(
                title=data['title'],
                defaults={
                    'value': data['value'],
                    'icon': data['icon'],
                    'index': data['index'],
                }
            )

        # 创建示例活动
        activities_data = [
            {
                'title': '社区清洁日',
                'description': '一起来美化我们的社区环境',
                'content': '让我们携手清理社区，创造更好的生活环境。',
                'start_time': timezone.now(),
                'end_time': timezone.now() + timezone.timedelta(days=7),
                'location': '阳光社区',
                'volunteers_needed': 20,
                'is_featured': True,
            },
            {
                'title': '爱心助老活动',
                'description': '为社区老人提供关爱和服务',
                'content': '为独居老人提供生活帮助和心理关怀。',
                'start_time': timezone.now(),
                'end_time': timezone.now() + timezone.timedelta(days=30),
                'location': '夕阳红养老院',
                'volunteers_needed': 15,
                'is_featured': True,
            },
        ]

        self.stdout.write('创建示例活动...')
        for data in activities_data:
            Activity.objects.get_or_create(
                title=data['title'],
                defaults={
                    'description': data['description'],
                    'content': data['content'],
                    'start_time': data['start_time'],
                    'end_time': data['end_time'],
                    'location': data['location'],
                    'volunteers_needed': data['volunteers_needed'],
                    'is_featured': data['is_featured'],
                }
            )

        self.stdout.write(self.style.SUCCESS('数据填充完成！'))
