"""
واجهة سطر الأوامر (CLI) لمكتبة Bflore
"""

import os
import sys
import argparse
import logging
import socket
import webbrowser
from http.server import HTTPServer, SimpleHTTPRequestHandler
from threading import Timer

logger = logging.getLogger('bflore.cli')
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

class BfloreHTTPRequestHandler(SimpleHTTPRequestHandler):
    """
    معالج HTTP مخصص لدعم الملفات العربية وتحسين العرض
    """
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def end_headers(self):
        self.send_header("Content-Type", self.get_content_type())
        self.send_header("X-Bflore-Server", "True")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("X-Frame-Options", "SAMEORIGIN")
        self.send_header("X-XSS-Protection", "1; mode=block")
        super().end_headers()
    
    def get_content_type(self):
        """تحديد نوع المحتوى المناسب مع دعم الملفات العربية"""
        content_type = super().guess_type(self.path)
        
        if content_type[0] == "text/html":
            return "text/html; charset=UTF-8"
        elif content_type[0] == "text/css":
            return "text/css; charset=UTF-8"
        elif content_type[0] == "application/javascript":
            return "application/javascript; charset=UTF-8"
        elif content_type[0] is None and self.path.endswith(".js"):
            return "application/javascript; charset=UTF-8"
        
        return content_type[0] or "application/octet-stream"
    
    def log_message(self, format, *args):
        """تسجيل رسائل الخادم بتنسيق Bflore"""
        logger.info(f"{self.address_string()} - {format % args}")

def setup_hosts_file(custom_name):
    """إعداد ملف المضيفين لدعم اسم المضيف المخصص"""
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
                return True
            except PermissionError:
                logger.warning(f"تعذر إضافة {custom_name} إلى ملف المضيفين. قد تحتاج إلى امتيازات المسؤول.")
                return False
    
    except Exception as e:
        logger.error(f"خطأ عند محاولة تعديل ملف المضيفين: {str(e)}")
        return False
    
    return True

def is_port_available(port):
    """التحقق من توفر المنفذ"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.bind(("127.0.0.1", port))
        result = True
    except:
        result = False
    finally:
        sock.close()
    return result

def find_available_port(start_port=8000):
    """البحث عن منفذ متاح"""
    port = start_port
    while not is_port_available(port):
        port += 1
        if port > start_port + 100:  # تجنب البحث إلى ما لا نهاية
            return None
    return port

def serve_directory(directory, custom_name, port, open_browser=True):
    """تشغيل خادم HTTP لمجلد محدد مع اسم مضيف مخصص"""
    # التأكد من أن المجلد موجود
    if not os.path.isdir(directory):
        logger.error(f"المجلد '{directory}' غير موجود")
        return False
    
    # تغيير المجلد الحالي
    os.chdir(directory)
    
    # إعداد الخادم
    try:
        server_address = ('127.0.0.1', port)
        httpd = HTTPServer(server_address, BfloreHTTPRequestHandler)
        url = f"http://{custom_name}:{port}"
        
        logger.info(f"بدء تشغيل خادم Bflore على {url}")
        logger.info(f"اضغط على Ctrl+C للخروج")
        
        # فتح المتصفح
        if open_browser:
            Timer(1, lambda: webbrowser.open(url)).start()
        
        # تشغيل الخادم
        httpd.serve_forever()
        
    except KeyboardInterrupt:
        logger.info("تم إيقاف الخادم بواسطة المستخدم")
    except Exception as e:
        logger.error(f"خطأ عند تشغيل الخادم: {str(e)}")
        return False
    
    return True

def main():
    """
    نقطة الدخول الرئيسية لواجهة سطر الأوامر
    """
    # إنشاء محلل المعلمات
    parser = argparse.ArgumentParser(
        description="Bflore - أداة لتشغيل المواقع المحلية مع أسماء مخصصة",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    
    parser.add_argument("--name", "-n", help="اسم المضيف المخصص للموقع", default="bflore")
    parser.add_argument("--port", "-p", type=int, help="منفذ الخادم", default=8080)
    parser.add_argument("--directory", "-d", help="مجلد الموقع", default=".")
    parser.add_argument("--no-browser", action="store_true", help="عدم فتح المتصفح تلقائيًا")
    parser.add_argument("--verbose", "-v", action="store_true", help="عرض معلومات تصحيح إضافية")
    
    # تحليل المعلمات
    args = parser.parse_args()
    
    # ضبط مستوى التسجيل
    if args.verbose:
        logger.setLevel(logging.DEBUG)
    
    # عرض شعار الترحيب
    print(r"""
    ╔══════════════════════════════════════════════╗
    ║                                              ║
    ║     ██████╗ ███████╗██╗      ██████╗ ██████╗ ║
    ║     ██╔══██╗██╔════╝██║     ██╔═══██╗██╔══██╗║
    ║     ██████╔╝█████╗  ██║     ██║   ██║██████╔╝║
    ║     ██╔══██╗██╔══╝  ██║     ██║   ██║██╔══██╗║
    ║     ██████╔╝██║     ███████╗╚██████╔╝██║  ██║║
    ║     ╚═════╝ ╚═╝     ╚══════╝ ╚═════╝ ╚═╝  ╚═╝║
    ║                                              ║
    ╚══════════════════════════════════════════════╝
    """)
    
    # التحقق من صحة الاسم المخصص
    custom_name = args.name
    if not all(c.isalnum() or c == '-' for c in custom_name):
        logger.warning("الاسم المخصص يجب أن يحتوي على أحرف وأرقام وشرطات فقط. استخدام 'localhost' بدلاً من ذلك.")
        custom_name = "localhost"
    
    # التحقق من توفر المنفذ
    port = args.port
    if not is_port_available(port):
        new_port = find_available_port(port)
        if new_port:
            logger.warning(f"المنفذ {port} غير متاح. استخدام المنفذ {new_port} بدلاً من ذلك.")
            port = new_port
        else:
            logger.error(f"لم يتم العثور على منفذ متاح")
            return 1
    
    # إعداد ملف المضيفين إذا كان الاسم مخصصًا
    if custom_name != "localhost":
        if not setup_hosts_file(custom_name):
            logger.warning(f"تعذر إعداد اسم المضيف المخصص. استخدام 'localhost' بدلاً من ذلك.")
            custom_name = "localhost"
    
    # بدء تشغيل الخادم
    success = serve_directory(
        directory=args.directory,
        custom_name=custom_name,
        port=port,
        open_browser=not args.no_browser
    )
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())