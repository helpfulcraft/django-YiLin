# 益邻 - 社区服务平台

益邻是一个基于Django开发的社区服务平台，旨在为社区居民提供便捷的服务和帮助。

## 功能特点

- 志愿者活动管理
- 新闻资讯发布
- 服务项目管理
- 在线咨询
- 帮助中心
- 用户管理系统

## 技术栈

- Django 4.2
- Bootstrap 5
- SQLite3
- Redis (缓存)
- Celery (异步任务)
- CKEditor (富文本编辑器)

## 部署说明

1. 克隆项目
```bash
git clone https://github.com/helpfulcraft/django-YiLin.git
cd django-YiLin
```

2. 安装依赖
```bash
pip install -r requirements.txt
```

3. 配置环境变量
```bash
cp .env.example .env
# 编辑.env文件，填写必要的配置信息
```

4. 初始化数据库
```bash
python manage.py migrate
python manage.py createsuperuser
python create_help_data.py
```

5. 收集静态文件
```bash
python manage.py collectstatic
```

6. 启动服务器
```bash
python manage.py runserver
```

## 开发指南

1. 创建虚拟环境
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

2. 安装开发依赖
```bash
pip install -r requirements.txt
```

3. 运行测试
```bash
pytest
```

## 贡献指南

1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情
