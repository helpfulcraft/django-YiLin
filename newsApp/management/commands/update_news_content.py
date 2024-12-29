# -*- coding: utf-8 -*-
import os
import sys
import django
from django.core.management.base import BaseCommand
from django.conf import settings

# Add the project root to the Python path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.append(project_root)

# Explicitly set the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'welfare_config.settings')
django.setup()

from newsApp.models import News

class Command(BaseCommand):
    help = 'Update news content with comprehensive information'

    def handle(self, *args, **kwargs):
        # Define news content dictionary
        news_updates = {
            1: {
                'title': '养老全景：中国养老服务体系发展报告',
                'summary': '深入解析中国养老服务体系的现状、挑战与未来发展趋势',
                'content': '''
                <h2>中国养老服务体系全景报告</h2>
                <p>随着人口老龄化的加速，中国养老服务体系正面临前所未有的挑战与机遇。本报告全面梳理了当前养老服务的发展现状，并对未来趋势进行深入分析。</p>
                
                <h3>人口结构变化</h3>
                <p>据最新统计数据显示，中国60岁以上老年人口已超过2.6亿，占总人口的18.7%。这一数据意味着每5个中国人中就有1个老年人，养老服务的需求迫在眉睫。</p>
                
                <h3>养老服务体系建设</h3>
                <ul>
                    <li>政府大力推进"居家养老"和"社区养老"模式</li>
                    <li>鼓励社会资本参与养老服务市场</li>
                    <li>加强养老服务专业人才培养</li>
                </ul>
                
                <h3>未来展望</h3>
                <p>预计到2035年，中国将基本建成与经济社会发展水平相适应、覆盖全面、保障充分的养老服务体系。</p>
                '''
            },
            2: {
                'title': '智慧养老模式创新与实践',
                'summary': '科技赋能养老服务，打造更智能、更人性化的养老生态',
                'content': '''
                <h2>智慧养老：科技改变养老服务</h2>
                <p>随着人工智能、大数据和物联网技术的快速发展，智慧养老正成为养老服务创新的重要方向。</p>
                
                <h3>智慧养老的关键技术</h3>
                <ul>
                    <li>远程健康监测系统</li>
                    <li>智能家居辅助设备</li>
                    <li>AI个性化服务推荐</li>
                    <li>虚拟陪伴机器人</li>
                </ul>
                
                <h3>典型案例</h3>
                <p>北京、上海等城市已开始试点智慧养老社区，通过信息化手段提升老年人生活质量。</p>
                
                <h3>技术应用场景</h3>
                <ol>
                    <li>健康状况实时监测</li>
                    <li>紧急救援快速响应</li>
                    <li>慢性病管理</li>
                    <li>心理健康关怀</li>
                </ol>
                '''
            },
            3: {
                'title': '养老服务标准化建设进展',
                'summary': '推动养老服务标准化，提升服务质量与专业水平',
                'content': '''
                <h2>养老服务标准化：提质增效</h2>
                <p>标准化是提升养老服务质量的关键路径。本文将详细解读养老服务标准化建设的最新进展。</p>
                
                <h3>标准化建设的重点领域</h3>
                <ul>
                    <li>服务人员职业资格标准</li>
                    <li>养老机构服务规范</li>
                    <li>老年人照护等级评估标准</li>
                    <li>养老服务设施建设标准</li>
                </ul>
                
                <h3>标准化带来的价值</h3>
                <ol>
                    <li>提高服务一致性</li>
                    <li>保障老年人权益</li>
                    <li>促进行业专业化发展</li>
                    <li>建立服务质量评价体系</li>
                </ol>
                
                <h3>未来展望</h3>
                <p>预计到2025年，将形成较为完善的养老服务标准体系，全面提升养老服务质量。</p>
                '''
            },
            4: {
                'title': '营养膳食指导与老年健康',
                'summary': '科学饮食，助力老年人健康长寿',
                'content': '''
                <h2>老年营养膳食指导</h2>
                <p>合理的营养是老年人健康的重要保障。本文将详细解读老年人营养膳食的科学指导。</p>
                
                <h3>老年人营养需求特点</h3>
                <ul>
                    <li>热量需求相对降低</li>
                    <li>蛋白质需求相对增加</li>
                    <li>微量元素吸收能力下降</li>
                </ul>
                
                <h3>推荐膳食结构</h3>
                <ol>
                    <li>优质蛋白：鱼、禽、蛋、豆制品</li>
                    <li>富含钙质食物：奶制品、深绿色蔬菜</li>
                    <li>富含维生素的水果蔬菜</li>
                    <li>适量全谷物</li>
                </ol>
                
                <h3>饮食建议</h3>
                <p>少盐、少糖、少油，多样化、均衡、规律饮食，保持良好的饮食习惯。</p>
                '''
            },
            5: {
                'title': '社区养老服务体系建设',
                'summary': '构建以社区为基础的养老服务网络，实现老年人就近照护',
                'content': '''
                <h2>社区养老：构建邻里互助新模式</h2>
                <p>社区养老正成为解决老年人照护需求的重要途径，本文将深入探讨社区养老服务体系建设。</p>
                
                <h3>社区养老服务模式</h3>
                <ul>
                    <li>日间照料中心</li>
                    <li>居家上门服务</li>
                    <li>邻里互助网络</li>
                    <li>志愿者服务</li>
                </ul>
                
                <h3>服务内容</h3>
                <ol>
                    <li>生活照料</li>
                    <li>健康管理</li>
                    <li>精神慰藉</li>
                    <li>文化娱乐</li>
                    <li>紧急救援</li>
                </ol>
                
                <h3>建设重点</h3>
                <p>整合社区资源，构建"15分钟养老服务圈"，让老年人享受便捷、温暖的养老服务。</p>
                '''
            },
            6: {
                'title': '医养结合服务模式探索',
                'summary': '整合医疗与养老资源，提供全方位的老年健康服务',
                'content': '''
                <h2>医养结合：健康养老的创新路径</h2>
                <p>医养结合是应对人口老龄化的重要战略，旨在为老年人提供连续、综合的医疗和养老服务。</p>
                
                <h3>医养结合的核心理念</h3>
                <ul>
                    <li>预防为主</li>
                    <li>早期干预</li>
                    <li>连续性照护</li>
                    <li>全程健康管理</li>
                </ul>
                
                <h3>服务模式</h3>
                <ol>
                    <li>医疗机构设立养老病区</li>
                    <li>养老机构内设医疗服务点</li>
                    <li>家庭医生签约服务</li>
                    <li>远程医疗监测</li>
                </ol>
                
                <h3>未来发展方向</h3>
                <p>推动医疗资源下沉，建立以老年人需求为中心的综合医养服务体系。</p>
                '''
            },
            7: {
                'title': '居家养老政策解读',
                'summary': '深入解析居家养老政策，助力老年人实现原地养老',
                'content': '''
                <h2>居家养老：政策支持与实施路径</h2>
                <p>居家养老是我国养老服务体系的重要组成部分，本文将全面解读相关政策与实施策略。</p>
                
                <h3>政策支持重点</h3>
                <ul>
                    <li>财政补贴</li>
                    <li>税收优惠</li>
                    <li>服务标准化</li>
                    <li>人才培养</li>
                </ul>
                
                <h3>居家养老服务内容</h3>
                <ol>
                    <li>生活照料</li>
                    <li>家政服务</li>
                    <li>康复护理</li>
                    <li>精神慰藉</li>
                    <li>紧急救援</li>
                </ol>
                
                <h3>政策目标</h3>
                <p>到2025年，基本建成以居家为基础、社区为依托、机构为补充的养老服务体系。</p>
                '''
            },
            8: {
                'title': '老年人心理健康关怀',
                'summary': '关注老年人心理健康，提升晚年生活质量',
                'content': '''
                <h2>老年人心理健康：温暖与尊严</h2>
                <p>心理健康是老年人生活质量的重要组成部分。本文将探讨老年人心理健康关怀的重要性。</p>
                
                <h3>常见心理健康问题</h3>
                <ul>
                    <li>孤独感</li>
                    <li>抑郁症</li>
                    <li>焦虑</li>
                    <li>认知功能下降</li>
                </ul>
                
                <h3>心理关怀策略</h3>
                <ol>
                    <li>社交活动</li>
                    <li>心理咨询</li>
                    <li>家庭支持</li>
                    <li>志愿者陪伴</li>
                    <li>兴趣培养</li>
                </ol>
                
                <h3>关怀理念</h3>
                <p>尊重、理解、陪伴，让老年人感受到社会的温暖与关爱。</p>
                '''
            },
            9: {
                'title': '养老服务数字化转型',
                'summary': '数字技术赋能养老服务，提升服务效率与质量',
                'content': '''
                <h2>养老服务数字化：技术赋能新时代</h2>
                <p>数字化转型正在深刻改变养老服务模式，为老年人提供更智能、更便捷的服务。</p>
                
                <h3>数字化转型的关键技术</h3>
                <ul>
                    <li>大数据分析</li>
                    <li>人工智能</li>
                    <li>物联网</li>
                    <li>云计算</li>
                </ul>
                
                <h3>应用场景</h3>
                <ol>
                    <li>智能健康监测</li>
                    <li>个性化服务推荐</li>
                    <li>远程医疗咨询</li>
                    <li>智能家居适老化改造</li>
                </ol>
                
                <h3>转型目标</h3>
                <p>构建以老年人需求为中心的数字化养老服务生态系统。</p>
                '''
            },
            10: {
                'title': '社会力量参与养老服务',
                'summary': '多元主体协同，共同构建现代养老服务体系',
                'content': '''
                <h2>社会力量：养老服务的重要支柱</h2>
                <p>社会力量的广泛参与是推动养老服务高质量发展的关键路径。本文将深入探讨多元主体协同的养老服务模式。</p>
                
                <h3>社会力量参与类型</h3>
                <ul>
                    <li>社会组织</li>
                    <li>企业</li>
                    <li>慈善机构</li>
                    <li>志愿者团队</li>
                </ul>
                
                <h3>参与方式</h3>
                <ol>
                    <li>提供专业服务</li>
                    <li>资金支持</li>
                    <li>志愿服务</li>
                    <li>技术创新</li>
                </ol>
                
                <h3>政策支持</h3>
                <p>鼓励和引导社会力量参与养老服务，构建多元共治的养老服务生态系统。</p>
                '''
            }
        }

        # Update news entries
        for pk, update_data in news_updates.items():
            try:
                news = News.objects.get(pk=pk)
                news.title = update_data['title']
                news.summary = update_data['summary']
                news.content = update_data['content']
                news.save()
                print(f'Successfully updated news entry {pk}: {news.title}')
            except News.DoesNotExist:
                print(f'News entry {pk} not found')
            except Exception as e:
                print(f'Error updating news entry {pk}: {e}')
