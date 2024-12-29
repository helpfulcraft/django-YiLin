from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from newsApp.models import NewsCategory, News
from django.utils import timezone

class Command(BaseCommand):
    help = '创建初始新闻数据'

    def handle(self, *args, **kwargs):
        # 创建或获取超级用户
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

        # 创建新闻分类
        categories = [
            {
                'name': '政策动态',
                'description': '养老服务相关政策法规和政府动态'
            },
            {
                'name': '行业资讯',
                'description': '养老服务行业最新动态和发展趋势'
            },
            {
                'name': '健康养老',
                'description': '健康养老知识和相关资讯'
            },
            {
                'name': '服务动态',
                'description': '平台服务动态和最新活动'
            }
        ]

        for cat_data in categories:
            NewsCategory.objects.get_or_create(
                name=cat_data['name'],
                defaults={'description': cat_data['description']}
            )

        # 获取分类对象
        policy_cat = NewsCategory.objects.get(name='政策动态')
        industry_cat = NewsCategory.objects.get(name='行业资讯')
        health_cat = NewsCategory.objects.get(name='健康养老')
        service_cat = NewsCategory.objects.get(name='服务动态')

        # 创建新闻
        news_data = [
            {
                'title': '国务院办公厅印发《"十四五"养老服务体系规划》',
                'category': policy_cat,
                'summary': '近日，国务院办公厅印发《"十四五"养老服务体系规划》，明确了"十四五"时期养老服务体系建设的主要目标和重点任务。',
                'content': '''
                <h2>重要政策解读</h2>
                <p>《规划》提出，到2025年，养老服务体系更加完善，服务能力明显提升，服务质量持续改善。基本养老服务制度框架建立，养老服务供给更加充沛，市场活力充分激发，养老服务人才队伍不断壮大，服务质量持续改善，服务消费潜力持续释放，老年人的获得感、幸福感、安全感不断提升。</p>
                <h3>主要目标</h3>
                <ul>
                    <li>养老服务床位总量持续扩大，每千名老年人拥有养老床位数达到35张以上</li>
                    <li>护理型床位占比达到55%以上</li>
                    <li>养老机构护理员配备比例达到1:4以上</li>
                    <li>养老服务从业人员总量超过500万人</li>
                </ul>
                <h3>重点任务</h3>
                <ol>
                    <li><strong>构建居家社区机构相协调的养老服务网络</strong>
                        <p>推动居家、社区、机构养老融合发展，完善以居家为基础、社区为依托、机构为补充、医养相结合的养老服务体系。</p>
                    </li>
                    <li><strong>完善养老服务基本制度</strong>
                        <p>建立健全基本养老服务清单制度，推动建立老年人能力评估制度，完善养老服务补贴制度。</p>
                    </li>
                    <li><strong>提升养老服务质量</strong>
                        <p>加强养老服务质量监管，建立健全养老服务标准和评价体系，推进养老服务人才培养。</p>
                    </li>
                </ol>
                ''',
                'is_pinned': True,
                'views': 156
            },
            {
                'title': '智慧养老新模式：科技赋能养老服务创新发展',
                'category': industry_cat,
                'summary': '随着科技的发展，智慧养老正在成为养老服务的新趋势。本文将探讨如何利用现代科技提升养老服务质量。',
                'content': '''
                <h2>智慧养老的发展现状</h2>
                <p>随着人工智能、物联网、大数据等技术的快速发展，智慧养老正在重塑传统养老服务模式。越来越多的养老机构开始采用智能化设备和系统，为老年人提供更优质的服务。</p>
                <h3>主要应用领域</h3>
                <ol>
                    <li><strong>健康监测</strong>
                        <p>通过穿戴设备实时监测老年人的身体状况，包括心率、血压、睡眠质量等指标，及时发现健康隐患。</p>
                    </li>
                    <li><strong>安全保障</strong>
                        <p>利用智能传感器、摄像头等设备，构建全方位的安全防护网，实现跌倒检测、异常行为识别等功能。</p>
                    </li>
                    <li><strong>生活照护</strong>
                        <p>引入智能机器人辅助日常生活照料，提供送餐、清洁、陪伴等服务。</p>
                    </li>
                    <li><strong>远程医疗</strong>
                        <p>通过远程诊疗系统，实现在线问诊、健康咨询、用药指导等服务。</p>
                    </li>
                </ol>
                ''',
                'views': 89
            },
            {
                'title': '老年人营养膳食指南：科学饮食助力健康养老',
                'category': health_cat,
                'summary': '合理的营养膳食是健康养老的重要基础。本文将为您详细介绍老年人的营养需求和科学饮食方案。',
                'content': '''
                <h2>老年人营养需求特点</h2>
                <p>随着年龄增长，老年人的身体机能逐渐下降，营养需求也发生相应变化。科学的营养膳食对维护老年人健康具有重要意义。</p>
                <h3>基本营养原则</h3>
                <ol>
                    <li><strong>能量需求</strong>
                        <p>由于活动量减少，能量需求相应降低，但要注意避免营养不良。建议：</p>
                        <ul>
                            <li>主食以细粮为主，粗细搭配</li>
                            <li>控制总热量，预防肥胖</li>
                        </ul>
                    </li>
                    <li><strong>蛋白质补充</strong>
                        <p>适当增加优质蛋白质的摄入，推荐：</p>
                        <ul>
                            <li>瘦肉、鱼、禽肉</li>
                            <li>鸡蛋、奶制品</li>
                            <li>豆类及其制品</li>
                        </ul>
                    </li>
                </ol>
                ''',
                'views': 245
            },
            {
                'title': '我平台推出"关爱老人"系列公益活动',
                'category': service_cat,
                'summary': '为进一步提升养老服务质量，促进社区养老服务发展，我平台即将开展"关爱老人"系列公益活动。',
                'content': '''
                <h2>活动背景</h2>
                <p>为了更好地服务社区老年人，提升其生活质量和幸福感，我平台特别策划了"关爱老人"系列公益活动。本次活动将联合多家社会组织，为社区老年人提供多样化的服务和关爱。</p>
                <h3>活动内容</h3>
                <ol>
                    <li><strong>健康义诊活动</strong>
                        <p>联合社区医院开展义诊活动：</p>
                        <ul>
                            <li>免费体检</li>
                            <li>健康咨询</li>
                            <li>用药指导</li>
                            <li>康复建议</li>
                        </ul>
                    </li>
                    <li><strong>文化娱乐活动</strong>
                        <p>组织丰富多彩的文化活动：</p>
                        <ul>
                            <li>书法绘画班</li>
                            <li>歌唱班</li>
                            <li>太极班</li>
                            <li>手工艺制作</li>
                        </ul>
                    </li>
                </ol>
                ''',
                'is_pinned': True,
                'views': 178
            }
        ]

        for news_item in news_data:
            News.objects.get_or_create(
                title=news_item['title'],
                defaults={
                    'author': admin_user,
                    'category': news_item['category'],
                    'summary': news_item['summary'],
                    'content': news_item['content'],
                    'status': 'published',
                    'views': news_item.get('views', 0),
                    'is_pinned': news_item.get('is_pinned', False)
                }
            )

        self.stdout.write(self.style.SUCCESS('Successfully created news data'))
