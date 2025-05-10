# مكتبة Bflore 🌺

مكتبة Python تعمل كإضافة لإطار Flask لتسهيل تطوير المواقع المحلية مع دعم للروابط المخصصة.

## المميزات الرئيسية

- **روابط مخصصة**: استخدام أسماء مضيفين مخصصة بدلاً من "localhost" مثل `http://ihab:8080`
- **دعم كامل للغة العربية**: تعامل صحيح مع النصوص العربية في HTML، CSS وملفات JavaScript
- **واجهة سطر أوامر**: تشغيل أي مشروع ويب على رابط مخصص بسهولة
- **تكامل مع Flask**: يعمل كإضافة لمشاريع Flask الحالية دون تعديلات كبيرة
- **فتح تلقائي للمتصفح**: يفتح المتصفح تلقائيًا على الرابط المحلي المخصص

## التثبيت

```bash
pip install bflore
```

## الاستخدام مع Flask

```python
from flask import Flask
from bflore import BfloreApp, run_with_custom_host

# إنشاء تطبيق Bflore بدلاً من Flask
app = BfloreApp(__name__)

@app.route('/')
def hello():
    return "مرحبًا بك في تطبيق Bflore!"

if __name__ == '__main__':
    # تشغيل التطبيق باستخدام اسم مضيف مخصص
    app.run_with_custom_host('ihab', port=8080)
```

أو يمكنك استخدام تطبيق Flask الحالي:

```python
from flask import Flask
from bflore import run_with_custom_host

app = Flask(__name__)

@app.route('/')
def hello():
    return "مرحبًا بك في تطبيق Flask!"

if __name__ == '__main__':
    # تشغيل تطبيق Flask باستخدام Bflore
    run_with_custom_host(app, 'ihab', port=8080)
```

## استخدام واجهة سطر الأوامر

يمكنك تشغيل أي مشروع ويب محلي (HTML/CSS/JS) باستخدام الأمر التالي:

```bash
# في مجلد المشروع
bflore --name ihab --port 8080
```

أو بالشكل المختصر:

```bash
bflore -n ihab -p 8080
```

### خيارات سطر الأوامر

- `--name`, `-n`: اسم المضيف المخصص (افتراضيًا "bflore")
- `--port`, `-p`: رقم المنفذ (افتراضيًا 8080)
- `--directory`, `-d`: مجلد المشروع (افتراضيًا المجلد الحالي)
- `--no-browser`: عدم فتح المتصفح تلقائيًا
- `--verbose`, `-v`: إظهار معلومات إضافية للتصحيح

## معالجة النصوص العربية

تقوم المكتبة تلقائيًا بمعالجة النصوص العربية من خلال:

1. إضافة ترميز UTF-8 في ملفات HTML
2. إضافة اتجاه RTL عند اكتشاف نصوص عربية
3. استخدام خطوط مناسبة للغة العربية
4. تعديل إعدادات Flask لدعم الأحرف العربية في JSON

## المتطلبات

- Python 3.6 أو أحدث
- Flask 2.0.0 أو أحدث

## ترخيص

هذه المكتبة متاحة تحت رخصة MIT. انظر ملف LICENSE للمزيد من التفاصيل.