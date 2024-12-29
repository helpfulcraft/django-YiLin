from django.db import migrations
from django.utils import timezone
from datetime import timedelta

def add_initial_data(apps, schema_editor):
    Banner = apps.get_model('home', 'Banner')
    Statistics = apps.get_model('home', 'Statistics')

    # 添加示例轮播图
    banners = [
        {
            'title': '欢迎来到福祉网站',
            'subtitle': '为老年人提供优质的养老服务',
            'description': '我们致力于为老年人提供全方位的养老服务和信息支持',
            'order': 1,
            'start_time': timezone.now(),
            'end_time': timezone.now() + timedelta(days=365),
        },
        {
            'title': '志愿服务招募',
            'subtitle': '加入我们的志愿者团队',
            'description': '为老年人提供关爱和帮助，让爱心传递',
            'order': 2,
            'start_time': timezone.now(),
            'end_time': timezone.now() + timedelta(days=365),
        },
        {
            'title': '养老服务介绍',
            'subtitle': '专业的养老服务团队',
            'description': '提供专业的养老服务，让老年人安享晚年',
            'order': 3,
            'start_time': timezone.now(),
            'end_time': timezone.now() + timedelta(days=365),
        }
    ]

    for banner_data in banners:
        Banner.objects.create(**banner_data)

    # 添加示例统计数据
    statistics = [
        {
            'title': '注册用户',
            'value': 1000,
            'icon': 'bi bi-people',
            'order': 1,
        },
        {
            'title': '志愿者活动',
            'value': 50,
            'icon': 'bi bi-heart',
            'order': 2,
        },
        {
            'title': '服务项目',
            'value': 30,
            'icon': 'bi bi-briefcase',
            'order': 3,
        },
        {
            'title': '累计服务时长',
            'value': 5000,
            'icon': 'bi bi-clock',
            'order': 4,
        }
    ]

    for stat_data in statistics:
        Statistics.objects.create(**stat_data)

def remove_initial_data(apps, schema_editor):
    Banner = apps.get_model('home', 'Banner')
    Statistics = apps.get_model('home', 'Statistics')
    
    Banner.objects.all().delete()
    Statistics.objects.all().delete()

class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_banner_statistics_delete_carousel'),
    ]

    operations = [
        migrations.RunPython(add_initial_data, remove_initial_data),
    ]
