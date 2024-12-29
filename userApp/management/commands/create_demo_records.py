from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from serviceApp.models import Service, ServiceCategory, ServiceAppointment
from volunteerApp.models import VolunteerActivity, ActivityCategory, VolunteerApplication
import random
from datetime import timedelta

class Command(BaseCommand):
    help = '创建示例服务记录和志愿记录'

    def handle(self, *args, **kwargs):
        # 创建服务类别
        service_categories = [
            {'name': '居家养老', 'description': '为老年人提供居家养老服务', 'icon': 'fa-home'},
            {'name': '医疗保健', 'description': '提供基础医疗保健服务', 'icon': 'fa-heartbeat'},
            {'name': '心理咨询', 'description': '提供心理健康咨询服务', 'icon': 'fa-brain'},
        ]
        
        for cat_data in service_categories:
            category, created = ServiceCategory.objects.get_or_create(
                name=cat_data['name'],
                defaults={
                    'description': cat_data['description'],
                    'icon': cat_data['icon']
                }
            )
            if created:
                self.stdout.write(f'创建服务类别: {category.name}')

        # 创建服务项目
        services = [
            {
                'name': '上门护理',
                'category': '居家养老',
                'price': 100,
                'duration': '2小时',
                'short_description': '提供专业的上门护理服务'
            },
            {
                'name': '健康体检',
                'category': '医疗保健',
                'price': 200,
                'duration': '1小时',
                'short_description': '提供基础健康检查服务'
            },
            {
                'name': '心理辅导',
                'category': '心理咨询',
                'price': 150,
                'duration': '1小时',
                'short_description': '提供一对一心理咨询服务'
            },
        ]

        for service_data in services:
            category = ServiceCategory.objects.get(name=service_data['category'])
            service, created = Service.objects.get_or_create(
                name=service_data['name'],
                defaults={
                    'category': category,
                    'price': service_data['price'],
                    'duration': service_data['duration'],
                    'short_description': service_data['short_description'],
                    'content': service_data['short_description'],
                }
            )
            if created:
                self.stdout.write(f'创建服务项目: {service.name}')

        # 创建志愿活动类别
        activity_categories = [
            {'name': '社区服务', 'description': '服务社区居民'},
            {'name': '环境保护', 'description': '保护环境，美化家园'},
            {'name': '教育支持', 'description': '支持教育事业发展'},
        ]

        for cat_data in activity_categories:
            category, created = ActivityCategory.objects.get_or_create(
                name=cat_data['name'],
                defaults={'description': cat_data['description']}
            )
            if created:
                self.stdout.write(f'创建志愿活动类别: {category.name}')

        # 创建志愿活动
        activities = [
            {
                'title': '社区清洁日',
                'category': '环境保护',
                'description': '组织社区清洁活动，美化环境',
                'required_volunteers': 10
            },
            {
                'title': '爱心课堂',
                'category': '教育支持',
                'description': '为困难学生提供免费课业辅导',
                'required_volunteers': 5
            },
            {
                'title': '敬老服务',
                'category': '社区服务',
                'description': '为社区老人提供生活帮助',
                'required_volunteers': 8
            },
        ]

        for activity_data in activities:
            category = ActivityCategory.objects.get(name=activity_data['category'])
            activity, created = VolunteerActivity.objects.get_or_create(
                title=activity_data['title'],
                defaults={
                    'category': category,
                    'description': activity_data['description'],
                    'required_volunteers': activity_data['required_volunteers'],
                    'start_time': timezone.now() + timedelta(days=7),
                    'end_time': timezone.now() + timedelta(days=8),
                    'status': 'published',
                    'location': '社区活动中心'
                }
            )
            if created:
                self.stdout.write(f'创建志愿活动: {activity.title}')

        # 为每个用户创建服务记录和志愿记录
        users = User.objects.all()
        status_choices = ['pending', 'confirmed', 'completed', 'cancelled']
        
        for user in users:
            # 创建服务记录
            services = Service.objects.all()
            for service in services:
                appointment, created = ServiceAppointment.objects.get_or_create(
                    user=user,
                    service=service,
                    defaults={
                        'appointment_time': timezone.now() + timedelta(days=random.randint(1, 30)),
                        'status': random.choice(status_choices),
                        'note': '这是一条示例服务记录'
                    }
                )
                if created:
                    self.stdout.write(f'为用户 {user.username} 创建服务记录: {service.name}')

            # 创建志愿记录
            activities = VolunteerActivity.objects.all()
            for activity in activities:
                application, created = VolunteerApplication.objects.get_or_create(
                    user=user,
                    activity=activity,
                    defaults={
                        'status': random.choice(['pending', 'approved', 'rejected']),
                        'message': '这是一条示例志愿申请'
                    }
                )
                if created:
                    self.stdout.write(f'为用户 {user.username} 创建志愿记录: {activity.title}')

        self.stdout.write(self.style.SUCCESS('成功创建示例数据'))
