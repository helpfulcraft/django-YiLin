from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from userApp.models import Notification
from django.utils import timezone
from datetime import timedelta

class Command(BaseCommand):
    help = '创建示例通知数据'

    def handle(self, *args, **options):
        # 获取所有用户
        users = User.objects.all()
        
        for user in users:
            # 系统通知
            Notification.objects.create(
                user=user,
                title='欢迎来到福祉网站',
                message='感谢您注册福祉网站！这里有许多志愿服务机会等待您的参与。',
                notification_type='info',
                created_at=timezone.now() - timedelta(days=7)
            )
            
            # 身份验证通知
            Notification.objects.create(
                user=user,
                title='请完善您的身份信息',
                message='为了保障服务质量，请您尽快完善身份认证信息。',
                notification_type='warning',
                url='/user/profile/',
                created_at=timezone.now() - timedelta(days=5)
            )
            
            # 活动通知
            Notification.objects.create(
                user=user,
                title='新的志愿服务机会',
                message='您关注的领域有新的志愿服务机会，快来看看吧！',
                notification_type='info',
                url='/volunteer/',
                created_at=timezone.now() - timedelta(days=3)
            )
            
            # 系统维护通知
            Notification.objects.create(
                user=user,
                title='系统维护通知',
                message='系统将于本周日凌晨2:00-4:00进行例行维护，期间可能无法访问。',
                notification_type='warning',
                created_at=timezone.now() - timedelta(days=1)
            )
            
            # 成功通知
            Notification.objects.create(
                user=user,
                title='志愿服务时长已更新',
                message='您参与的"社区关爱老人"活动服务时长已认证，获得4小时志愿服务时长。',
                notification_type='success',
                url='/user/volunteer-hours/',
                created_at=timezone.now() - timedelta(hours=12)
            )
            
        self.stdout.write(self.style.SUCCESS('成功创建示例通知'))
