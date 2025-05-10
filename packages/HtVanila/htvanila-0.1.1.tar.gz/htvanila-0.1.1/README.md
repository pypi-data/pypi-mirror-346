# HtVanila

![HtVanila Banner](https://img.shields.io/badge/HtVanila-v0.1.0-brightgreen)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python: 3.7+](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://www.python.org/downloads/)

أداة قوية لدمج ملفات HTML و CSS و JavaScript والصور في ملف HTML واحد (*مكتفي ذاتيًا*). تستخدم هذه المكتبة لإنشاء ملفات HTML مستقلة يمكن مشاركتها بسهولة.

<div align="center">
  <pre>
   _   _ _     __   _       _  _ 
  | | | | \ \ / /  / \    | \| |
  | |_| |  \ V /  / _ \   | .` |
  |  _  |   \ V / / ___ \  | |\ |
  |_| |_|    \_/ /_/   \_\ |_| \_|
  </pre>
</div>

## 🚀 المميزات

- ✅ دمج ملفات HTML و CSS و JavaScript في ملف واحد
- ✅ تضمين الصور كتشفير base64 داخل الملف الناتج
- ✅ تكامل سلس مع إطار Flask (لتحسين أداء التطبيقات)
- ✅ أداة سطر أوامر سهلة الاستخدام
- ✅ وضع تلقائي لاكتشاف الملفات في المشروع
- ✅ محسن أداء لتقليل حجم الملفات الناتجة
- ✅ مكتبة برمجية يمكن استخدامها في المشاريع

## 📦 التثبيت

```bash
pip install HtVanila
```

أو التثبيت من المصدر:

```bash
git clone https://github.com/username/HtVanila.git
cd HtVanila
pip install -e .
```

## 🔍 نظرة سريعة على الاستخدام

### استخدام سطر الأوامر

```bash
# الوضع التلقائي (اكتشاف الملفات في المجلد الحالي)
vanila --auto --output combined.html

# تحديد الملفات يدويًا
vanila --html index.html --css style.css --js script.js --img images --output combined.html
```

### استخدام المكتبة البرمجية

```python
from htvanila import combine_html

# دمج ملفات وحفظ النتيجة
combine_html(
    html_file='index.html',
    css_files=['style.css', 'theme.css'],
    js_files=['script.js', 'app.js'],
    img_dir='images',
    output_file='combined.html'
)
```

### التكامل مع Flask

```python
from flask import Flask
from htvanila import flask_integration

app = Flask(__name__)
# دمج القوالب تلقائيًا عند بدء التطبيق
flask_integration(app, template_dir='templates')

@app.route('/')
def index():
    return render_template('index.html')
```

## 📘 دليل الاستخدام المفصل

### 🔸 استخدام أداة سطر الأوامر

أداة سطر الأوامر `vanila` تتيح لك دمج ملفات الويب بسهولة:

```bash
# عرض المساعدة
vanila --help

# الوضع التلقائي
vanila --auto

# تحديد الملفات يدويًا
vanila --html index.html --css style.css --js script.js --img images
```

#### الخيارات المتاحة:

- `--html`, `-h`: تحديد ملف HTML الرئيسي
- `--css`, `-c`: تحديد ملفات CSS (يمكن تكرار هذا الخيار لتحديد عدة ملفات)
- `--js`, `-j`: تحديد ملفات JavaScript (يمكن تكرار هذا الخيار لتحديد عدة ملفات)
- `--img`, `-i`: تحديد مجلد الصور
- `--output`, `-o`: تحديد ملف الإخراج
- `--auto`, `-a`: تفعيل الوضع التلقائي لاكتشاف الملفات

### 🔸 استخدام المكتبة في البرامج

#### دمج الملفات برمجيًا:

```python
from htvanila import combine_html

# طريقة أساسية
result = combine_html(
    html_file='index.html',
    css_files=['style.css'],
    js_files=['script.js'],
    img_dir='images',
    output_file='combined.html'
)

# يمكن استخدام النتيجة مباشرة كنص
print(result)
```

#### تحسين أداء ملفات HTML:

```python
from htvanila import optimize_html

# تحسين محتوى HTML
with open('index.html', 'r', encoding='utf-8') as f:
    html_content = f.read()

optimized_html = optimize_html(
    html_content,
    minify=True,                # تقليص الكود
    remove_comments=True,       # إزالة التعليقات
    combine_assets=True         # دمج الأصول المضمنة
)

# حفظ الملف المحسن
with open('optimized.html', 'w', encoding='utf-8') as f:
    f.write(optimized_html)
```

#### التكامل مع Flask:

```python
from flask import Flask, render_template
from htvanila import flask_integration

app = Flask(__name__)

# دمج ملفات القوالب تلقائيًا
flask_integration(app, template_dir='templates')

@app.route('/')
def index():
    # الآن render_template ستستخدم القوالب المدمجة
    return render_template('index.html', title='صفحة البداية')

if __name__ == '__main__':
    app.run(debug=True)
```

### 🔸 معالجة مجلد كامل

يمكنك معالجة مجلد كامل من ملفات HTML وتحويلها إلى ملفات مدمجة:

```python
from htvanila.core import process_directory

# معالجة جميع ملفات HTML في المجلد
process_directory(
    input_dir='src',        # مجلد المصدر
    output_dir='dist'       # مجلد الإخراج
)
```

## 🌟 أمثلة متقدمة

### مثال 1: استخدام الوضع التلقائي مع CLI

هيكل المشروع:
```
my_project/
├── index.html
├── css/
│   └── style.css
├── js/
│   └── app.js
└── images/
    ├── logo.png
    └── banner.jpg
```

تنفيذ الأمر:
```bash
cd my_project
vanila --auto --output dist/index-standalone.html
```

### مثال 2: دمج موقع متعدد الصفحات

```python
import os
from htvanila import combine_html

# مجلدات المشروع
project_dir = 'website'
output_dir = 'dist'
os.makedirs(output_dir, exist_ok=True)

# ملفات HTML الرئيسية
html_files = [
    'index.html',
    'about.html',
    'contact.html'
]

# ملفات مشتركة
common_css = ['css/common.css', 'css/theme.css']
common_js = ['js/main.js']

# معالجة كل صفحة
for html_file in html_files:
    input_path = os.path.join(project_dir, html_file)
    output_path = os.path.join(output_dir, html_file)
    
    # تحديد ملفات CSS و JS الخاصة بالصفحة
    page_name = os.path.splitext(html_file)[0]
    page_css = common_css + [f'css/{page_name}.css']
    page_js = common_js + [f'js/{page_name}.js']
    
    # فلترة الملفات غير الموجودة
    page_css = [f for f in page_css if os.path.exists(os.path.join(project_dir, f))]
    page_js = [f for f in page_js if os.path.exists(os.path.join(project_dir, f))]
    
    # دمج الملفات
    combine_html(
        html_file=input_path,
        css_files=page_css,
        js_files=page_js,
        img_dir=os.path.join(project_dir, 'images'),
        output_file=output_path
    )
    
    print(f"تم إنشاء الملف المدمج: {output_path}")
```

### مثال 3: تكامل Flask مع تحسين الأداء

```python
from flask import Flask, render_template
from htvanila import flask_integration
from htvanila.optimizer import optimize

app = Flask(__name__)

# دمج ملفات القوالب
flask_integration(app, template_dir='templates')

# تسجيل دالة لتحسين جميع استجابات HTML
@app.after_request
def optimize_html_response(response):
    if response.content_type == 'text/html':
        response.set_data(
            optimize(
                response.get_data(as_text=True),
                minify=True,
                remove_comments=True,
                combine_assets=True
            )
        )
    return response

@app.route('/')
def index():
    return render_template('index.html')
```

## 🛠️ سير العمل المقترح

1. **التطوير**: طور موقعك باستخدام ملفات منفصلة (HTML, CSS, JS) للحفاظ على التنظيم والقابلية للصيانة.

2. **الاختبار**: اختبر موقعك بالشكل المعتاد.

3. **الإنتاج**: استخدم `HtVanila` لدمج جميع الملفات في ملف HTML واحد مكتفي ذاتيًا.

4. **النشر**: قم بنشر الملف المدمج للإنتاج.

## 🤔 الأسئلة الشائعة

### س: هل يؤثر تضمين الصور كـ base64 على الأداء؟
ج: نعم، يمكن أن يزيد من حجم الملف، لكنه يقلل من عدد طلبات HTTP. هذا مفيد للمواقع الصغيرة والتطبيقات التي تحتاج إلى مشاركة ملف واحد.

### س: هل يمكنني استثناء بعض الملفات الخارجية من الدمج؟
ج: نعم، المكتبة تتجاهل الملفات المرتبطة بـ URLs (مثل CDN)، وتدمج فقط الملفات المحلية.

### س: هل تدعم المكتبة المصادر الخارجية مثل Google Fonts؟
ج: نعم، الروابط الخارجية تبقى كما هي دون تغيير.

## 📋 قائمة المهام المستقبلية

- [ ] دعم تضمين الخطوط (Web Fonts)
- [ ] تحسين ضغط الصور قبل التضمين
- [ ] إضافة خيارات لتنظيف وتحسين الكود
- [ ] توفير واجهة مستخدم رسومية للأداة
- [ ] دعم الترميز لملفات CSS و JS

## 📄 الترخيص

هذا المشروع مرخص تحت [رخصة MIT](https://opensource.org/licenses/MIT).

## 👥 المساهمة

مساهماتك مرحب بها! لا تتردد في:

1. تشعيب المشروع (Fork)
2. إنشاء فرع للميزة الجديدة (`git checkout -b feature/amazing-feature`)
3. ارتكاب التغييرات (`git commit -m 'إضافة ميزة رائعة'`)
4. دفع الفرع (`git push origin feature/amazing-feature`)
5. فتح طلب سحب (Pull Request)

## 📞 الاتصال

- **المطور**: Developer
- **البريد الإلكتروني**: acounts687@gmail.com
- **GitHub**: [https://github.com/MODIgimar](#)

---

<div align="center">
  <small>🌟 صنع بكل ❤️ للمطورين 🌟</small>
</div>