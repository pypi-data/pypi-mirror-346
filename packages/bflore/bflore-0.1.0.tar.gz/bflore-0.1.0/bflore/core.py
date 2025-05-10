"""
ملف النواة الأساسية لمكتبة Bflore - يحتوي على الوظائف الرئيسية للمكتبة
"""

import os
import socket
import webbrowser
from threading import Timer
from urllib.parse import urlparse
import logging
from flask import Flask

# إعداد المسجل للمكتبة
logger = logging.getLogger('bflore')
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

class BfloreApp:
    """
    الفئة الرئيسية التي تمثل تطبيق Bflore الذي يعتمد على Flask
    """
    
    def __init__(self, import_name, static_folder=None, template_folder=None, 
                 static_url_path=None, instance_path=None, instance_relative_config=False, 
                 root_path=None):
        """
        إنشاء تطبيق Bflore جديد يعتمد على Flask
        
        المعلمات:
            import_name: اسم الوحدة التي يتم استدعاء التطبيق منها
            static_folder: مجلد الملفات الثابتة
            template_folder: مجلد القوالب
            static_url_path: مسار URL للملفات الثابتة
            instance_path: مسار مثيل التطبيق
            instance_relative_config: ما إذا كان التكوين مرتبطًا بمسار المثيل
            root_path: المسار الجذر للتطبيق
        """
        self.flask_app = Flask(import_name, 
                              static_folder=static_folder, 
                              template_folder=template_folder,
                              static_url_path=static_url_path,
                              instance_path=instance_path,
                              instance_relative_config=instance_relative_config,
                              root_path=root_path)
        
        # دعم الحروف العربية
        self.flask_app.config['JSON_AS_ASCII'] = False
        self.flask_app.config['BFLORE_CUSTOM_HOST'] = None
        
        # نقل جميع الطرق من تطبيق Flask إلى كائن BfloreApp
        for attr_name in dir(self.flask_app):
            if not attr_name.startswith('__'):
                attr = getattr(self.flask_app, attr_name)
                if callable(attr) and not hasattr(self, attr_name):
                    setattr(self, attr_name, attr)
    
    def run_with_custom_host(self, custom_name, port=5000, open_browser=True, **options):
        """
        تشغيل التطبيق باستخدام اسم مضيف مخصص
        
        المعلمات:
            custom_name: اسم المضيف المخصص الذي تريد استخدامه
            port: منفذ الخادم
            open_browser: ما إذا كان سيتم فتح المتصفح تلقائيًا
            **options: خيارات إضافية يتم تمريرها إلى طريقة run في Flask
        """
        # التحقق من صحة الاسم المخصص
        if not custom_name.isalnum():
            logger.warning("الاسم المخصص يجب أن يحتوي على أحرف وأرقام فقط. استخدام 'localhost' بدلاً من ذلك.")
            custom_name = "localhost"
        
        # إضافة إدخال إلى ملف hosts
        hosts_path = r"C:\Windows\System32\drivers\etc\hosts" if os.name == "nt" else "/etc/hosts"
        host_entry = f"127.0.0.1 {custom_name}"
        
        try:
            # التحقق من وجود الإدخال
            add_entry = True
            if os.path.exists(hosts_path):
                with open(hosts_path, 'r') as file:
                    if host_entry in file.read():
                        add_entry = False
            
            # إضافة الإدخال إذا لزم الأمر
            if add_entry:
                try:
                    with open(hosts_path, 'a') as file:
                        file.write(f"\n{host_entry}")
                    logger.info(f"تمت إضافة {custom_name} إلى ملف المضيفين")
                except PermissionError:
                    logger.warning(f"تعذر إضافة {custom_name} إلى ملف المضيفين. قد تحتاج إلى امتيازات المسؤول.")
                    logger.info(f"استخدام localhost بدلاً من ذلك.")
                    custom_name = "localhost"
        
        except Exception as e:
            logger.error(f"خطأ عند محاولة تعديل ملف المضيفين: {str(e)}")
            logger.info(f"استخدام localhost بدلاً من ذلك.")
            custom_name = "localhost"
        
        # حفظ اسم المضيف المخصص في التكوين
        self.flask_app.config['BFLORE_CUSTOM_HOST'] = custom_name
        
        # إنشاء URL للفتح في المتصفح
        url = f"http://{custom_name}:{port}"
        
        # فتح المتصفح إذا تم تحديد ذلك
        if open_browser:
            Timer(1, lambda: webbrowser.open(url)).start()
        
        # تشغيل تطبيق Flask مع الخيارات المحددة
        logger.info(f"بدء تشغيل التطبيق على {url}")
        return self.flask_app.run(host="127.0.0.1", port=port, **options)

# دالة مساعدة للتحقق من توفر المنفذ
def is_port_available(port):
    """
    التحقق مما إذا كان المنفذ المحدد متاحًا للاستخدام
    
    المعلمات:
        port: رقم المنفذ للتحقق منه
        
    العوائد:
        bool: True إذا كان المنفذ متاحًا، False خلاف ذلك
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = False
    try:
        sock.bind(("127.0.0.1", port))
        result = True
    except:
        pass
    finally:
        sock.close()
    return result

# دالة مختصرة لتشغيل التطبيق مع اسم مضيف مخصص
def run_with_custom_host(app, custom_name, port=5000, open_browser=True, **options):
    """
    دالة مساعدة لتشغيل أي تطبيق Flask مع اسم مضيف مخصص
    
    المعلمات:
        app: تطبيق Flask أو BfloreApp
        custom_name: اسم المضيف المخصص
        port: منفذ الخادم
        open_browser: ما إذا كان سيتم فتح المتصفح تلقائيًا
        **options: خيارات إضافية يتم تمريرها إلى طريقة run
    """
    if isinstance(app, BfloreApp):
        return app.run_with_custom_host(custom_name, port, open_browser, **options)
    
    # إذا كان تطبيق Flask عادي، نقوم بتغليفه في BfloreApp
    bflore_app = BfloreApp(app.import_name)
    bflore_app.flask_app = app
    return bflore_app.run_with_custom_host(custom_name, port, open_browser, **options)