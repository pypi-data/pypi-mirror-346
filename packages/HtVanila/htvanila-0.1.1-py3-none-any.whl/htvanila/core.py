# htvanila/core.py
import os
import re
import base64
import mimetypes
from bs4 import BeautifulSoup
from .utils import setup_logging, get_file_content, is_url, file_to_base64

logger = setup_logging()

def combine_files(html_file, css_files=None, js_files=None, img_dir=None):
    """دمج ملفات HTML و CSS و JS والصور في ملف HTML واحد"""
    if css_files is None:
        css_files = []
    if js_files is None:
        js_files = []
    
    logger.info(f"معالجة ملف HTML: {html_file}")
    
    try:
        with open(html_file, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # إضافة CSS
        for css_file in css_files:
            logger.info(f"إضافة ملف CSS: {css_file}")
            css_content = get_file_content(css_file)
            style_tag = soup.new_tag('style')
            style_tag.string = css_content
            soup.head.append(style_tag)
        
        # إضافة JavaScript
        for js_file in js_files:
            logger.info(f"إضافة ملف JS: {js_file}")
            js_content = get_file_content(js_file)
            script_tag = soup.new_tag('script')
            script_tag.string = js_content
            soup.body.append(script_tag)
        
        # تضمين الصور
        if img_dir and os.path.exists(img_dir):
            logger.info(f"معالجة الصور من المجلد: {img_dir}")
            for img_tag in soup.find_all('img'):
                src = img_tag.get('src')
                if src and not is_url(src):
                    img_path = os.path.join(img_dir, os.path.basename(src))
                    if os.path.exists(img_path):
                        base64_str = file_to_base64(img_path)
                        mime_type = mimetypes.guess_type(img_path)[0] or 'image/png'
                        img_tag['src'] = f"data:{mime_type};base64,{base64_str}"
                        logger.info(f"تم تضمين الصورة: {img_path}")
        
        # تضمين CSS المرتبط في الملف الرئيسي
        for link_tag in soup.find_all('link', rel='stylesheet'):
            href = link_tag.get('href')
            if href and not is_url(href):
                css_path = os.path.join(os.path.dirname(html_file), href)
                if os.path.exists(css_path):
                    logger.info(f"تضمين ملف CSS مرتبط: {css_path}")
                    css_content = get_file_content(css_path)
                    style_tag = soup.new_tag('style')
                    style_tag.string = css_content
                    link_tag.replace_with(style_tag)
        
        # تضمين JavaScript المرتبط في الملف الرئيسي
        for script_tag in soup.find_all('script', src=True):
            src = script_tag.get('src')
            if src and not is_url(src):
                js_path = os.path.join(os.path.dirname(html_file), src)
                if os.path.exists(js_path):
                    logger.info(f"تضمين ملف JS مرتبط: {js_path}")
                    js_content = get_file_content(js_path)
                    new_script = soup.new_tag('script')
                    new_script.string = js_content
                    script_tag.replace_with(new_script)
        
        return str(soup)
    
    except Exception as e:
        logger.error(f"حدث خطأ أثناء الدمج: {str(e)}")
        raise

def embed_flask_template(app, template_dir):
    """دمج ملفات التمبلت في Flask"""
    template_path = os.path.join(app.root_path, template_dir)
    logger.info(f"معالجة مجلد التمبلت: {template_path}")
    
    if not os.path.exists(template_path):
        logger.warning(f"مجلد التمبلت غير موجود: {template_path}")
        return
    
    # إنشاء نسخة من التمبلت المدمجة
    combined_dir = os.path.join(app.root_path, 'combined_templates')
    os.makedirs(combined_dir, exist_ok=True)
    
    # معالجة جميع ملفات HTML في مجلد التمبلت
    process_directory(template_path, combined_dir)
    
    # تغيير مسار التمبلت في Flask
    app.template_folder = 'combined_templates'
    logger.info(f"تم تحديث مسار التمبلت إلى: {combined_dir}")

def process_directory(input_dir, output_dir):
    """معالجة جميع ملفات HTML في مجلد معين"""
    for root, _, files in os.walk(input_dir):
        for file in files:
            if file.endswith('.html'):
                html_file = os.path.join(root, file)
                rel_path = os.path.relpath(root, input_dir)
                output_subdir = os.path.join(output_dir, rel_path)
                os.makedirs(output_subdir, exist_ok=True)
                
                output_file = os.path.join(output_subdir, file)
                
                # البحث عن ملفات CSS و JS المرتبطة
                base_name = os.path.splitext(html_file)[0]
                css_file = f"{base_name}.css"
                js_file = f"{base_name}.js"
                
                css_files = [css_file] if os.path.exists(css_file) else []
                js_files = [js_file] if os.path.exists(js_file) else []
                
                # البحث عن مجلد الصور
                img_dir = os.path.join(os.path.dirname(html_file), 'images')
                if not os.path.exists(img_dir):
                    img_dir = os.path.join(os.path.dirname(html_file), 'img')
                
                if not os.path.exists(img_dir):
                    img_dir = None
                
                result = combine_files(html_file, css_files, js_files, img_dir)
                
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(result)
                
                logger.info(f"تم إنشاء الملف المدمج: {output_file}")