# Generated by Django 4.2 on 2024-12-28 13:09

from django.db import migrations

def add_initial_data(apps, schema_editor):
    HelpCategory = apps.get_model('helpApp', 'HelpCategory')
    HelpArticle = apps.get_model('helpApp', 'HelpArticle')
    FAQ = apps.get_model('helpApp', 'FAQ')
    Guide = apps.get_model('helpApp', 'Guide')

    # 创建帮助分类
    account_category = HelpCategory.objects.create(
        name='账号相关',
        description='账号注册、登录、信息修改等相关问题',
        icon='fas fa-user',
        order=1
    )

    service_category = HelpCategory.objects.create(
        name='服务预约',
        description='服务预约、取消、评价等相关问题',
        icon='fas fa-calendar-check',
        order=2
    )

    volunteer_category = HelpCategory.objects.create(
        name='志愿服务',
        description='志愿者报名、活动参与等相关问题',
        icon='fas fa-hands-helping',
        order=3
    )

    feedback_category = HelpCategory.objects.create(
        name='投诉建议',
        description='问题反馈、投诉建议等相关问题',
        icon='fas fa-comment-dots',
        order=4
    )

    # 创建帮助文章
    HelpArticle.objects.create(
        category=account_category,
        title='如何注册新账号',
        content='<h4>注册步骤</h4><ol><li>点击网站右上角的"注册"按钮</li><li>填写用户名、邮箱和密码</li><li>点击"注册"完成账号创建</li></ol>',
        is_published=True
    )

    HelpArticle.objects.create(
        category=service_category,
        title='服务预约指南',
        content='<h4>预约步骤</h4><ol><li>浏览服务列表</li><li>选择需要的服务</li><li>选择预约时间</li><li>确认预约信息</li><li>提交预约申请</li></ol>',
        is_published=True
    )

    # 创建常见问题
    FAQ.objects.create(
        category=account_category,
        question='忘记密码怎么办？',
        answer='您可以通过以下步骤重置密码：<ol><li>点击登录页面的"忘记密码"链接</li><li>输入注册时使用的邮箱</li><li>在邮箱中查收重置密码链接</li><li>点击链接设置新密码</li></ol>',
        order=1,
        is_published=True
    )

    FAQ.objects.create(
        category=service_category,
        question='如何取消预约？',
        answer='您可以在"个人中心-服务记录"中找到需要取消的预约，点击"取消预约"按钮即可。请注意，预约开始前24小时内取消可能会影响您的信用记录。',
        order=1,
        is_published=True
    )

    # 创建使用指南
    Guide.objects.create(
        category=volunteer_category,
        title='如何成为志愿者',
        content='<h4>成为志愿者的步骤</h4><ol><li>完善个人资料</li><li>提交志愿者申请</li><li>等待审核通过</li><li>参加志愿者培训</li><li>开始参与志愿活动</li></ol>',
        order=1,
        is_published=True
    )

    Guide.objects.create(
        category=feedback_category,
        title='如何提交反馈',
        content='<h4>提交反馈的方式</h4><ol><li>在网站底部点击"反馈"</li><li>选择反馈类型</li><li>详细描述问题或建议</li><li>提交反馈</li><li>等待工作人员回复</li></ol>',
        order=1,
        is_published=True
    )

def remove_initial_data(apps, schema_editor):
    HelpCategory = apps.get_model('helpApp', 'HelpCategory')
    HelpCategory.objects.all().delete()

class Migration(migrations.Migration):

    dependencies = [
        ('helpApp', '0002_guide_faq'),
    ]

    operations = [
        migrations.RunPython(add_initial_data, remove_initial_data),
    ]
