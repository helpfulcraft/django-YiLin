from django.core.management.base import BaseCommand
from django.utils import timezone
from home.models import Carousel
from django.core.files import File
import os
from django.conf import settings

class Command(BaseCommand):
    help = '创建示例数据'

    def handle(self, *args, **kwargs):
        # 创建轮播图数据
        carousel_data = [
            {
                'title': '志愿者招募',
                'description': '加入我们的志愿者团队，让爱心传递得更远',
                'image': 'carousel/volunteer.jpg',
                'link': '/volunteer/activities/',
                'order': 1
            },
            {
                'title': '居家养老服务',
                'description': '专业的居家养老服务，让老年生活更舒心',
                'image': 'carousel/elderly-care.jpg',
                'link': '/service/home-care/',
                'order': 2
            },
            {
                'title': '社区文化活动',
                'description': '丰富多彩的社区活动，让生活更有趣',
                'image': 'carousel/community.jpg',
                'link': '/news/events/',
                'order': 3
            },
            {
                'title': '健康义诊服务',
                'description': '定期健康检查，预防胜于治疗',
                'image': 'carousel/health.jpg',
                'link': '/service/health-check/',
                'order': 4
            }
        ]

        for item in carousel_data:
            # 检查图片文件是否存在
            image_path = os.path.join(settings.MEDIA_ROOT, item['image'])
            if not os.path.exists(image_path):
                self.stdout.write(self.style.WARNING(f"图片文件不存在: {image_path}"))
                continue

            # 创建或更新轮播图
            carousel, created = Carousel.objects.get_or_create(
                title=item['title'],
                defaults={
                    'description': item['description'],
                    'link': item['link'],
                    'order': item['order']
                }
            )

            # 设置图片
            with open(image_path, 'rb') as f:
                carousel.image.save(os.path.basename(item['image']), File(f), save=True)

            action = '创建' if created else '更新'
            self.stdout.write(self.style.SUCCESS(f"{action}轮播图: {item['title']}"))
