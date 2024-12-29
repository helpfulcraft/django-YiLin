#!/bin/bash

# 安装依赖
pip install -r requirements.txt

# 收集静态文件
python manage.py collectstatic --noinput

# 运行数据库迁移
python manage.py migrate

# 创建超级用户（如果需要）
# python manage.py createsuperuser --noinput

# 运行初始化数据脚本
python create_help_data.py

# 启动Gunicorn服务器
gunicorn welfare_config.wsgi:application
