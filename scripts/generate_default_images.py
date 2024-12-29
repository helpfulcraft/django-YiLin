import os
from PIL import Image, ImageDraw, ImageFont
import sys

def create_default_image(filename, text, size=(800, 400), bg_color=(240, 240, 240), text_color=(100, 100, 100)):
    """创建默认图片"""
    img = Image.new('RGB', size, bg_color)
    draw = ImageDraw.Draw(img)
    
    # 尝试加载字体，如果失败则使用默认字体
    try:
        font = ImageFont.truetype("arial.ttf", 40)
    except:
        font = ImageFont.load_default()
    
    # 计算文本位置使其居中
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    x = (size[0] - text_width) // 2
    y = (size[1] - text_height) // 2
    
    # 绘制文本
    draw.text((x, y), text, font=font, fill=text_color)
    
    return img

def main():
    # 确保images目录存在
    images_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static', 'images')
    os.makedirs(images_dir, exist_ok=True)
    
    # 定义需要创建的默认图片
    default_images = {
        'logo.png': ('福祉网站', (200, 60)),
        'default_avatar.png': ('用户头像', (200, 200)),
        'default_banner.jpg': ('欢迎访问福祉网站', (1200, 400)),
        'default_activity.jpg': ('志愿活动', (800, 400)),
        'default_news.jpg': ('新闻资讯', (800, 400)),
        'default_service.jpg': ('养老服务', (800, 400)),
        'favicon.ico': ('福', (32, 32))
    }
    
    # 创建每个默认图片
    for filename, (text, size) in default_images.items():
        img = create_default_image(filename, text, size)
        img.save(os.path.join(images_dir, filename))
        print(f'Created {filename}')

if __name__ == '__main__':
    main()
