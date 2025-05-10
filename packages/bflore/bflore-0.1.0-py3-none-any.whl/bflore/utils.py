"""
أدوات مساعدة لمكتبة Bflore
"""

import os
import re
import sys
import socket
import logging
from pathlib import Path

logger = logging.getLogger('bflore.utils')

def sanitize_hostname(hostname):
    """
    تنظيف اسم المضيف للتأكد من أنه صالح
    
    المعلمات:
        hostname: اسم المضيف المراد تنظيفه
        
    العوائد:
        str: اسم المضيف المنظف
    """
    # إزالة الأحرف غير المسموح بها
    sanitized = re.sub(r'[^a-zA-Z0-9\-]', '', hostname)
    
    # التأكد من أن الاسم لا يبدأ أو ينتهي بشرطة
    sanitized = sanitized.strip('-')
    
    # إذا كان الاسم فارغًا، استخدم "bflore" كقيمة افتراضية
    if not sanitized:
        sanitized = "bflore"
    
    return sanitized

def find_project_root(start_dir=None):
    """
    البحث عن الجذر المحتمل للمشروع بناءً على ملفات شائعة
    
    المعلمات:
        start_dir: المجلد البدء للبحث، افتراضيًا المجلد الحالي
        
    العوائد:
        Path: مسار جذر المشروع
    """
    if not start_dir:
        start_dir = Path.cwd()
    else:
        start_dir = Path(start_dir)
    
    # ملفات تشير عادة إلى جذر المشروع
    root_indicators = [
        'index.html',
        'package.json',
        'requirements.txt',
        'setup.py',
        '.git',
        '.gitignore',
        'README.md',
        'app.py',
        'main.py'
    ]
    
    current = start_dir
    
    # البحث حتى 5 مستويات للأعلى
    for _ in range(5):
        for indicator in root_indicators:
            if (current / indicator).exists():
                return current
        
        # التحرك للمجلد الأعلى
        parent = current.parent
        if parent == current:  # وصلنا إلى الجذر
            break
        current = parent
    
    # إذا لم نجد جذرًا محتملًا، نعود إلى المجلد الأصلي
    return start_dir

def detect_project_type(directory):
    """
    اكتشاف نوع المشروع في المجلد المحدد
    
    المعلمات:
        directory: مسار المجلد للتحقق منه
        
    العوائد:
        str: نوع المشروع ('web', 'python', 'node', 'unknown')
    """
    directory = Path(directory)
    
    # مشروع ويب
    if (directory / 'index.html').exists():
        return 'web'
    
    # مشروع Python
    if (directory / 'requirements.txt').exists() or \
       (directory / 'setup.py').exists() or \
       list(directory.glob('*.py')):
        return 'python'
    
    # مشروع Node.js
    if (directory / 'package.json').exists():
        return 'node'
    
    # غير معروف
    return 'unknown'

def get_local_ip():
    """
    الحصول على عنوان IP المحلي للجهاز
    
    العوائد:
        str: عنوان IP المحلي
    """
    try:
        # إنشاء اتصال مؤقت للحصول على عنوان IP المحلي
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except:
        return "127.0.0.1"

def is_arabic_text(text):
    """
    التحقق مما إذا كان النص يحتوي على حروف عربية
    
    المعلمات:
        text: النص للتحقق منه
        
    العوائد:
        bool: True إذا كان النص يحتوي على حروف عربية
    """
    # نطاق Unicode للأحرف العربية
    arabic_pattern = re.compile(r'[\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF]+')
    return bool(arabic_pattern.search(text))

def handle_arabic_in_html(html_content):
    """
    معالجة النص العربي في محتوى HTML لضمان العرض الصحيح
    
    المعلمات:
        html_content: محتوى HTML للمعالجة
        
    العوائد:
        str: محتوى HTML المعالج
    """
    # التأكد من وجود تحديد UTF-8 في الرأس
    if '<head>' in html_content and 'charset' not in html_content:
        html_content = html_content.replace(
            '<head>',
            '<head>\n    <meta charset="UTF-8">'
        )
    
    # إضافة اتجاه من اليمين إلى اليسار إذا تم اكتشاف نص عربي
    if is_arabic_text(html_content):
        # إضافة اتجاه إلى وسم body إذا كان موجودًا
        if '<body' in html_content and 'dir=' not in html_content:
            html_content = re.sub(
                r'<body([^>]*)>',
                r'<body\1 dir="rtl">',
                html_content
            )
        
        # إضافة نمط CSS للخطوط العربية
        if '<head>' in html_content and 'font-family' not in html_content:
            arabic_font_style = '''
    <style>
        body, h1, h2, h3, h4, h5, h6, p, span, div {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        
        [lang="ar"] {
            direction: rtl;
            text-align: right;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
    </style>
'''
            html_content = html_content.replace(
                '<head>',
                '<head>' + arabic_font_style
            )
    
    return html_content

def generate_project_structure(directory, include_files=True, max_depth=3):
    """
    إنشاء تمثيل نصي لهيكل المشروع
    
    المعلمات:
        directory: المجلد لإنشاء الهيكل منه
        include_files: ما إذا كان سيتم تضمين الملفات
        max_depth: الحد الأقصى لعمق المجلدات
        
    العوائد:
        str: تمثيل نصي لهيكل المشروع
    """
    directory = Path(directory)
    result = []
    
    def _add_directory(path, prefix='', depth=0):
        if depth > max_depth:
            return
        
        # إضافة المجلد الحالي
        result.append(f"{prefix}📁 {path.name}/")
        
        # الحصول على قائمة بالمحتويات وفرزها
        contents = list(path.iterdir())
        dirs = sorted([p for p in contents if p.is_dir()])
        files = sorted([p for p in contents if p.is_file()]) if include_files else []
        
        # مرور عبر الملفات والمجلدات
        items = dirs + files
        for i, item in enumerate(items):
            is_last = (i == len(items) - 1)
            new_prefix = prefix + ('└── ' if is_last else '├── ')
            next_prefix = prefix + ('    ' if is_last else '│   ')
            
            if item.is_dir():
                _add_directory(item, next_prefix, depth + 1)
            elif include_files:
                result.append(f"{new_prefix}📄 {item.name}")
    
    _add_directory(directory)
    return '\n'.join(result)