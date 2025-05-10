"""
وحدة الوسائط (Middleware) لمكتبة Bflore
"""

import re
from functools import wraps
from flask import request, Response, g
from .utils import is_arabic_text, handle_arabic_in_html

class ArabicSupportMiddleware:
    """
    وسيط لدعم اللغة العربية في تطبيقات Flask
    
    يقوم هذا الوسيط بالتأكد من معالجة المحتوى العربي بشكل صحيح
    في استجابات HTML، وإضافة الترميز والأنماط المناسبة.
    """
    
    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)
    
    def init_app(self, app):
        """
        تهيئة الوسيط مع تطبيق Flask
        
        المعلمات:
            app: تطبيق Flask للتهيئة معه
        """
        app.config.setdefault('BFLORE_ARABIC_SUPPORT', True)
        app.config.setdefault('BFLORE_FIX_ARABIC_HTML', True)
        app.config.setdefault('JSON_AS_ASCII', False)  # لدعم الأحرف العربية في JSON
        
        # إضافة دالة معالجة الاستجابة
        app.after_request(self._process_response)
    
    def _process_response(self, response):
        """
        معالجة استجابة HTTP لدعم المحتوى العربي
        
        المعلمات:
            response: كائن الاستجابة من Flask
            
        العوائد:
            Response: كائن الاستجابة المعدل
        """
        # تخطي المعالجة إذا كانت غير ممكنة في الإعدادات
        if not self.app.config.get('BFLORE_ARABIC_SUPPORT', True):
            return response
        
        # معالجة استجابات HTML فقط
        content_type = response.headers.get('Content-Type', '')
        if 'text/html' in content_type:
            # التأكد من تحديد الترميز الصحيح
            if 'charset' not in content_type:
                response.headers['Content-Type'] = 'text/html; charset=UTF-8'
            
            # معالجة المحتوى العربي في HTML إذا كان مطلوبًا
            if self.app.config.get('BFLORE_FIX_ARABIC_HTML', True):
                response_data = response.get_data(as_text=True)
                if response_data and is_arabic_text(response_data):
                    modified_data = handle_arabic_in_html(response_data)
                    response.set_data(modified_data)
        
        return response

def arabic_template_filter(func):
    """
    مرشح قوالب لمعالجة المحتوى العربي
    
    المعلمات:
        func: الدالة المراد تغليفها
        
    العوائد:
        function: الدالة المغلفة
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        if isinstance(result, str) and is_arabic_text(result):
            # إضافة السمات المناسبة للنص العربي
            if not re.search(r'<[^>]* lang=["\']ar["\']', result):
                result = f'<span lang="ar">{result}</span>'
        return result
    return wrapper

def setup_arabic_support(app):
    """
    دالة مساعدة لإعداد دعم اللغة العربية في تطبيق Flask
    
    المعلمات:
        app: تطبيق Flask للإعداد
    """
    # إضافة الوسيط
    ArabicSupportMiddleware(app)
    
    # إضافة مرشح للقوالب
    @app.template_filter('arabic')
    @arabic_template_filter
    def arabic_filter(text):
        """مرشح للتعامل مع النصوص العربية في القوالب"""
        return text
    
    # إضافة دالة مساعدة لاختبار النص العربي
    @app.template_global('is_arabic')
    def is_arabic_template(text):
        """دالة عامة للقوالب لاختبار ما إذا كان النص عربيًا"""
        return is_arabic_text(text)
    
    # تعديل إعدادات التطبيق
    app.config['JSON_AS_ASCII'] = False
    
    return app