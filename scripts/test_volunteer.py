import os
import sys
import django

# 设置Django环境
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'welfare_config.settings')
django.setup()

from django.contrib.auth.models import User
from volunteerApp.models import ActivityCategory, VolunteerActivity, VolunteerApplication
from django.utils import timezone
from datetime import timedelta

def create_test_data():
    # 创建测试用户
    user, created = User.objects.get_or_create(
        username='testuser',
        defaults={
            'email': 'test@example.com',
            'is_active': True
        }
    )
    if created:
        user.set_password('testpass123')
        user.save()
        print('Created test user')
    
    # 创建活动分类
    category, created = ActivityCategory.objects.get_or_create(
        name='测试分类',
        defaults={
            'description': '这是一个测试分类'
        }
    )
    if created:
        print('Created test category')
    
    # 创建志愿活动
    activity, created = VolunteerActivity.objects.get_or_create(
        title='测试活动',
        defaults={
            'description': '这是一个测试活动的描述',
            'category': category,
            'location': '测试地点',
            'start_time': timezone.now() + timedelta(days=1),
            'end_time': timezone.now() + timedelta(days=2),
            'required_volunteers': 5,
            'status': 'published'
        }
    )
    if created:
        print('Created test activity')
    
    # 创建志愿申请
    application, created = VolunteerApplication.objects.get_or_create(
        user=user,
        activity=activity,
        defaults={
            'status': 'pending',
            'message': '这是一个测试申请'
        }
    )
    if created:
        print('Created test application')

if __name__ == '__main__':
    create_test_data()
    print('Test data creation completed')
