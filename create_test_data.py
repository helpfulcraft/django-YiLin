import os
import django
from decimal import Decimal

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'welfare_config.settings')
django.setup()

from django.contrib.auth.models import User
from serviceApp.models import Service, ServiceCategory
from django.utils import timezone

def create_test_notifications():
    # 确保有测试用户
    user, created = User.objects.get_or_create(
        username='testuser',
        email='test@example.com'
    )
    if created:
        user.set_password('testpass123')
        user.save()
        print(f'Created test user: {user.username}')
    
    # 创建不同类型的通知
    notifications = [
        {
            'title': '欢迎使用福祉网站',
            'message': '感谢您注册我们的网站！这里有许多优质的福祉服务等待您的发现。',
            'notification_type': 'info',
            'url': '/service/'
        },
        {
            'title': '服务申请成功',
            'message': '您的居家照护服务申请已成功提交，我们的工作人员将尽快与您联系。',
            'notification_type': 'success',
            'url': '/service/detail/1/'
        },
        {
            'title': '请完善个人信息',
            'message': '为了给您提供更好的服务，请及时完善您的个人信息。',
            'notification_type': 'warning',
            'url': '/user/profile/'
        },
        {
            'title': '服务评价提醒',
            'message': '您最近使用了我们的服务，请给出您的宝贵意见，帮助我们改进服务质量。',
            'notification_type': 'info',
            'url': '/service/feedback/'
        }
    ]
    
    for notif in notifications:
        # create_notification(user=user, **notif)
        print(f'Created notification: {notif["title"]}')

def create_test_services():
    # 创建服务类别
    categories = [
        {
            'name': '居家照护',
            'description': '提供专业的居家照护服务，包括生活照料、康复护理等',
            'icon': 'fas fa-home',
            'index': 1
        },
        {
            'name': '医疗保健',
            'description': '提供专业的医疗保健服务，包括健康咨询、中医调理等',
            'icon': 'fas fa-heartbeat',
            'index': 2
        },
        {
            'name': '心理咨询',
            'description': '提供专业的心理咨询服务，帮助缓解心理压力',
            'icon': 'fas fa-brain',
            'index': 3
        },
        {
            'name': '康复训练',
            'description': '提供专业的康复训练服务，帮助恢复身体机能',
            'icon': 'fas fa-dumbbell',
            'index': 4
        },
        {
            'name': '文化娱乐',
            'description': '提供丰富的文化娱乐活动，丰富精神文化生活',
            'icon': 'fas fa-music',
            'index': 5
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
            print(f'Created category: {category.name}')
    
    # 创建服务
    services = [
        {
            'name': '居家护理服务',
            'short_description': '专业护理人员上门提供生活照料和护理服务',
            'content': '''
                <h3>服务内容</h3>
                <ul>
                    <li>生活起居照料</li>
                    <li>卫生清洁服务</li>
                    <li>康复护理指导</li>
                    <li>用药提醒服务</li>
                </ul>
                <h3>服务特点</h3>
                <p>由经验丰富的护理人员提供专业的居家护理服务，让您在家也能享受到优质的照护。</p>
            ''',
            'category': '居家照护',
            'price': Decimal('200.00'),
            'duration': '2小时',
            'is_featured': True
        },
        {
            'name': '中医保健咨询',
            'short_description': '专业中医师提供健康咨询和调理建议',
            'content': '''
                <h3>服务内容</h3>
                <ul>
                    <li>中医体质辨识</li>
                    <li>养生保健指导</li>
                    <li>饮食调理建议</li>
                    <li>穴位按摩指导</li>
                </ul>
                <h3>服务特点</h3>
                <p>资深中医师根据个人体质特点，提供专业的养生保健和调理建议。</p>
            ''',
            'category': '医疗保健',
            'price': Decimal('300.00'),
            'duration': '1小时',
            'is_featured': True
        },
        {
            'name': '心理疏导服务',
            'short_description': '专业心理咨询师提供一对一心理辅导',
            'content': '''
                <h3>服务内容</h3>
                <ul>
                    <li>心理健康评估</li>
                    <li>情绪管理辅导</li>
                    <li>压力缓解技巧</li>
                    <li>家庭关系调适</li>
                </ul>
                <h3>服务特点</h3>
                <p>由持证心理咨询师提供专业的心理疏导服务，帮助您缓解心理压力。</p>
            ''',
            'category': '心理咨询',
            'price': Decimal('400.00'),
            'duration': '1小时',
            'is_featured': False
        },
        {
            'name': '康复理疗服务',
            'short_description': '提供专业的康复训练和理疗服务',
            'content': '''
                <h3>服务内容</h3>
                <ul>
                    <li>功能评估</li>
                    <li>运动训练</li>
                    <li>物理治疗</li>
                    <li>康复指导</li>
                </ul>
                <h3>服务特点</h3>
                <p>配备先进的康复设备，由专业康复师提供个性化的康复训练计划。</p>
            ''',
            'category': '康复训练',
            'price': Decimal('350.00'),
            'duration': '1.5小时',
            'is_featured': False
        },
        {
            'name': '老年文化活动',
            'short_description': '组织丰富多彩的文化娱乐活动',
            'content': '''
                <h3>活动内容</h3>
                <ul>
                    <li>书法创作</li>
                    <li>绘画活动</li>
                    <li>棋牌娱乐</li>
                    <li>文化沙龙</li>
                </ul>
                <h3>活动特点</h3>
                <p>定期组织各类文化活动，丰富老年人的精神文化生活，促进社交互动。</p>
            ''',
            'category': '文化娱乐',
            'price': Decimal('100.00'),
            'duration': '3小时',
            'is_featured': True
        }
    ]
    
    for service_data in services:
        category = ServiceCategory.objects.get(name=service_data['category'])
        service_data['category'] = category
        service, created = Service.objects.get_or_create(
            name=service_data['name'],
            defaults={
                'short_description': service_data['short_description'],
                'content': service_data['content'],
                'category': service_data['category'],
                'price': service_data['price'],
                'duration': service_data['duration'],
                'is_featured': service_data['is_featured'],
                'status': 'active'
            }
        )
        if created:
            print(f'Created service: {service.name}')

if __name__ == '__main__':
    print('Creating test data...')
    create_test_notifications()
    create_test_services()
    print('Test data creation completed!')
