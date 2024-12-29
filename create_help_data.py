import os
import django
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'welfare_config.settings')
django.setup()

from helpApp.models import HelpCategory, HelpArticle, FAQ, Guide

def create_help_data():
    # 创建帮助分类
    categories = [
        {
            'name': '新手指南',
            'description': '帮助新用户快速了解和使用福祉网站'
        },
        {
            'name': '服务指南',
            'description': '关于各类服务的详细说明和使用方法'
        },
        {
            'name': '账户安全',
            'description': '账户安全相关问题和解决方案'
        },
        {
            'name': '常见问题',
            'description': '用户经常遇到的问题和解答'
        }
    ]
    
    for cat_data in categories:
        category, created = HelpCategory.objects.get_or_create(
            name=cat_data['name'],
            defaults={'description': cat_data['description']}
        )
        if created:
            print(f'Created category: {category.name}')
    
    # 创建帮助文章
    articles = [
        {
            'title': '如何注册账号',
            'content': '''
## 注册步骤

1. 点击网站右上角的"注册"按钮
2. 填写用户名、邮箱和密码
3. 点击"注册"完成账号创建
4. 验证邮箱（可选）

## 注意事项

- 用户名不能包含特殊字符
- 密码长度至少8位
- 建议使用真实邮箱以便接收重要通知
            ''',
            'category': '新手指南',
            'is_published': True
        },
        {
            'title': '如何申请服务',
            'content': '''
## 申请服务流程

1. 登录您的账号
2. 浏览服务列表，选择需要的服务
3. 点击"申请服务"按钮
4. 填写服务申请表单
5. 等待工作人员联系

## 温馨提示

- 请确保填写真实信息
- 特殊需求可在备注中说明
- 如有疑问可联系客服
            ''',
            'category': '服务指南',
            'is_published': True
        }
    ]
    
    for article_data in articles:
        category = HelpCategory.objects.get(name=article_data['category'])
        article, created = HelpArticle.objects.get_or_create(
            title=article_data['title'],
            defaults={
                'content': article_data['content'],
                'category': category,
                'is_published': article_data['is_published'],
                'created_time': timezone.now()
            }
        )
        if created:
            print(f'Created article: {article.title}')
    
    # 创建FAQ
    faqs = [
        {
            'question': '忘记密码怎么办？',
            'answer': '''
点击登录页面的"忘记密码"链接，输入注册时使用的邮箱，我们会向您发送密码重置链接。
如果您没有收到邮件，请检查垃圾邮件文件夹或联系客服。
            ''',
            'category': '账户安全',
            'is_published': True
        },
        {
            'question': '如何修改个人信息？',
            'answer': '''
1. 登录账号后点击右上角的用户头像
2. 选择"个人设置"
3. 在相应的表单中修改信息
4. 点击"保存"完成修改
            ''',
            'category': '常见问题',
            'is_published': True
        }
    ]
    
    for faq_data in faqs:
        category = HelpCategory.objects.get(name=faq_data['category'])
        faq, created = FAQ.objects.get_or_create(
            question=faq_data['question'],
            defaults={
                'answer': faq_data['answer'],
                'category': category,
                'is_published': faq_data['is_published'],
                'created_time': timezone.now()
            }
        )
        if created:
            print(f'Created FAQ: {faq.question}')
    
    # 创建使用指南
    guides = [
        {
            'title': '网站功能介绍',
            'content': '''
## 主要功能

1. 服务申请
2. 志愿者活动
3. 新闻资讯
4. 在线咨询
5. 帮助中心

## 使用建议

- 建议先浏览新手指南
- 常见问题可在FAQ中找到答案
- 需要帮助可以联系在线客服
            ''',
            'category': '新手指南',
            'order': 1,
            'is_published': True
        },
        {
            'title': '服务类型说明',
            'content': '''
## 服务分类

1. 居家照护
2. 医疗陪护
3. 心理咨询
4. 生活援助

## 申请流程

1. 选择服务类型
2. 填写申请表
3. 等待审核
4. 确认服务时间
            ''',
            'category': '服务指南',
            'order': 2,
            'is_published': True
        }
    ]
    
    for guide_data in guides:
        category = HelpCategory.objects.get(name=guide_data['category'])
        guide, created = Guide.objects.get_or_create(
            title=guide_data['title'],
            defaults={
                'content': guide_data['content'],
                'category': category,
                'order': guide_data['order'],
                'is_published': guide_data['is_published'],
                'created_time': timezone.now()
            }
        )
        if created:
            print(f'Created guide: {guide.title}')

if __name__ == '__main__':
    print('Creating help center test data...')
    create_help_data()
    print('Done!')
