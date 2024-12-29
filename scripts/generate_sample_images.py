from PIL import Image
import os

def create_sample_image(filename, color=(70, 130, 180), size=(1920, 600)):
    # 创建一个纯色图片
    img = Image.new('RGB', size, color)
    img.save(filename)

def main():
    # 确保目录存在
    os.makedirs('media/carousel', exist_ok=True)
    
    # 创建示例图片，使用不同的颜色
    images = [
        ('volunteer.jpg', (70, 130, 180)),  # 蓝色
        ('elderly-care.jpg', (60, 179, 113)),  # 绿色
        ('community.jpg', (238, 130, 238)),  # 紫色
        ('health.jpg', (255, 165, 0))  # 橙色
    ]
    
    for filename, color in images:
        filepath = os.path.join('media/carousel', filename)
        create_sample_image(filepath, color)
        print(f'Created {filepath}')

if __name__ == '__main__':
    main()
