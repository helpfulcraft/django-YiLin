import os

def find_settings_file(start_path):
    for root, dirs, files in os.walk(start_path):
        if 'settings.py' in files:
            print(os.path.join(root, 'settings.py'))

find_settings_file('d:/Study/Vue-/福祉网站')
