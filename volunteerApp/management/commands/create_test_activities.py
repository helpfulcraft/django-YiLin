from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from volunteerApp.models import ActivityCategory, VolunteerActivity
from django.utils import timezone
from datetime import timedelta

class Command(BaseCommand):
    help = '创建测试志愿活动数据'

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

        # 创建活动分类
        categories = [
            {
                'name': '关爱老人',
                'description': '为老年人提供陪伴、聊天、生活协助等服务',
                'order': 1
            },
            {
                'name': '社区服务',
                'description': '参与社区环境改善、文化建设等活动',
                'order': 2
            },
            {
                'name': '健康关怀',
                'description': '协助开展健康讲座、体检活动等',
                'order': 3
            },
            {
                'name': '文化娱乐',
                'description': '组织文艺演出、兴趣班等活动',
                'order': 4
            }
        ]

        for cat_data in categories:
            category, created = ActivityCategory.objects.get_or_create(
                name=cat_data['name'],
                defaults={
                    'description': cat_data['description'],
                    'order': cat_data['order']
                }
            )
            if created:
                self.stdout.write(f'Created category: {category.name}')

        # 创建志愿活动
        activities = [
            {
                'category': '关爱老人',
                'title': '暖心陪伴计划',
                'description': '''
                    <h3>活动介绍</h3>
                    <p>为社区独居老人提供陪伴服务，包括聊天、读报、散步等活动。</p>
                    <h3>活动安排</h3>
                    <ul>
                        <li>上午：与老人聊天、读报</li>
                        <li>下午：陪老人散步、做简单运动</li>
                    </ul>
                    <h3>志愿者要求</h3>
                    <ul>
                        <li>有爱心、耐心</li>
                        <li>会与老年人沟通</li>
                        <li>时间充裕</li>
                    </ul>
                ''',
                'location': '幸福社区',
                'required_volunteers': 10,
                'current_volunteers': 5,
                'days_from_now': 7
            },
            {
                'category': '社区服务',
                'title': '社区环境美化行动',
                'description': '''
                    <h3>活动介绍</h3>
                    <p>组织志愿者参与社区环境整治，美化社区环境。</p>
                    <h3>活动内容</h3>
                    <ul>
                        <li>清理社区卫生死角</li>
                        <li>美化社区绿化带</li>
                        <li>设计制作社区文化墙</li>
                    </ul>
                    <h3>志愿者要求</h3>
                    <ul>
                        <li>身体健康</li>
                        <li>有责任心</li>
                        <li>能吃苦耐劳</li>
                    </ul>
                ''',
                'location': '和谐社区',
                'required_volunteers': 20,
                'current_volunteers': 8,
                'days_from_now': 14
            },
            {
                'category': '健康关怀',
                'title': '老年人健康讲座',
                'description': '''
                    <h3>活动介绍</h3>
                    <p>邀请专业医生为社区老年人开展健康知识讲座。</p>
                    <h3>活动内容</h3>
                    <ul>
                        <li>常见疾病预防</li>
                        <li>健康饮食指导</li>
                        <li>运动保健知识</li>
                    </ul>
                    <h3>志愿者要求</h3>
                    <ul>
                        <li>有医疗相关知识</li>
                        <li>表达能力强</li>
                        <li>有组织能力</li>
                    </ul>
                ''',
                'location': '康乐社区',
                'required_volunteers': 5,
                'current_volunteers': 2,
                'days_from_now': 21
            },
            {
                'category': '文化娱乐',
                'title': '欢乐艺术课堂',
                'description': '''
                    <h3>活动介绍</h3>
                    <p>为老年人开展书法、绘画等艺术课程。</p>
                    <h3>课程内容</h3>
                    <ul>
                        <li>书法基础教学</li>
                        <li>国画技法指导</li>
                        <li>艺术作品欣赏</li>
                    </ul>
                    <h3>志愿者要求</h3>
                    <ul>
                        <li>有艺术特长</li>
                        <li>有教学经验</li>
                        <li>善于沟通</li>
                    </ul>
                ''',
                'location': '文化社区',
                'required_volunteers': 8,
                'current_volunteers': 3,
                'days_from_now': 28
            }
        ]

        for activity_data in activities:
            category = ActivityCategory.objects.get(name=activity_data['category'])
            start_time = timezone.now() + timedelta(days=activity_data['days_from_now'])
            end_time = start_time + timedelta(hours=4)

            activity, created = VolunteerActivity.objects.get_or_create(
                title=activity_data['title'],
                defaults={
                    'category': category,
                    'description': activity_data['description'],
                    'location': activity_data['location'],
                    'start_time': start_time,
                    'end_time': end_time,
                    'required_volunteers': activity_data['required_volunteers'],
                    'current_volunteers': activity_data['current_volunteers'],
                    'status': 'published'
                }
            )
            if created:
                self.stdout.write(f'Created activity: {activity.title}')

        self.stdout.write(self.style.SUCCESS('Successfully created test volunteer activity data'))
