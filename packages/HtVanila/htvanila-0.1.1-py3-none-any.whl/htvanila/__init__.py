# htvanila/__init__.py
from .core import combine_files, embed_flask_template, process_directory
from .utils import setup_logging

__version__ = "0.1.0"

# الدالة الرئيسية للإستخدام المباشر مع Flask
def flask_integration(app, template_dir=None):
    """
    دمج ملفات HTML مع CSS و JS واستخدامها مع Flask
    
    يقوم بمعالجة ملفات التمبلت قبل تحميل التطبيق
    """
    if template_dir is None:
        template_dir = "templates"
    
    embed_flask_template(app, template_dir)
    return app

# الدالة الثانية: تحويل ملفات منفصلة إلى ملف HTML واحد برمجياً
def combine_html(html_file, css_files=None, js_files=None, img_dir=None, output_file=None):
    """
    دمج ملف HTML مع CSS و JS وتضمين الصور
    
    Args:
        html_file: مسار ملف HTML الرئيسي
        css_files: قائمة بمسارات ملفات CSS
        js_files: قائمة بمسارات ملفات JS
        img_dir: مجلد الصور للتضمين
        output_file: اسم ملف الإخراج
    """
    if css_files is None:
        css_files = []
    if js_files is None:
        js_files = []
    
    result = combine_files(html_file, css_files, js_files, img_dir)
    
    if output_file:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(result)
    
    return result

# الدالة الثالثة: محسن أداء لملفات HTML
def optimize_html(html_content, minify=True, remove_comments=True, combine_assets=True):
    """
    تحسين ملفات HTML وتقليل حجمها
    
    Args:
        html_content: محتوى HTML كنص
        minify: تقليص الكود
        remove_comments: إزالة التعليقات
        combine_assets: دمج الأصول المضمنة
    """
    from .optimizer import optimize
    return optimize(html_content, minify, remove_comments, combine_assets)