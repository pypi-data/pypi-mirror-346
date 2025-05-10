# htvanila/optimizer.py
import re
from bs4 import BeautifulSoup
import htmlmin

def optimize(html_content, minify=True, remove_comments=True, combine_assets=True):
    """
    تحسين ملف HTML وتقليل حجمه
    
    Args:
        html_content: محتوى HTML كنص
        minify: تقليص الكود
        remove_comments: إزالة التعليقات
        combine_assets: دمج الأصول المضمنة
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # إزالة التعليقات
    if remove_comments:
        comments = soup.find_all(string=lambda text: isinstance(text, str) and text.strip().startswith('<!--'))
        for comment in comments:
            comment.extract()
    
    # دمج الأصول المضمنة
    if combine_assets:
        # دمج جميع وسوم <style>
        styles = soup.find_all('style')
        if len(styles) > 1:
            combined_style = soup.new_tag('style')
            combined_content = ""
            
            for style in styles:
                if style.string:
                    combined_content += style.string + "\n"
                style.extract()
            
            combined_style.string = combined_content
            soup.head.append(combined_style)
        
        # دمج جميع وسوم <script> الداخلية
        scripts = soup.find_all('script', src=None)
        if len(scripts) > 1:
            combined_script = soup.new_tag('script')
            combined_content = ""
            
            for script in scripts:
                if script.string:
                    combined_content += script.string + ";\n"
                script.extract()
            
            combined_script.string = combined_content
            soup.body.append(combined_script)
    
    result = str(soup)
    
    # تقليص الكود
    if minify:
        result = htmlmin.minify(
            result,
            remove_comments=remove_comments,
            remove_empty_space=True,
            remove_optional_attribute_quotes=False
        )
    
    return result