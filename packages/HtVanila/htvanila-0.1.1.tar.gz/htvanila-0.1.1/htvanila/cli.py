# htvanila/cli.py
import os
import sys
import click
from colorama import Fore, Style, init
from .core import combine_files
from .utils import setup_logging, print_banner

init(autoreset=True)
logger = setup_logging()

def find_project_files(directory):
    """البحث عن ملفات المشروع في المجلد"""
    html_files = []
    css_files = []
    js_files = []
    img_dir = None

    # البحث عن ملفات HTML
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.html'):
                html_files.append(os.path.join(root, file))
            elif file.endswith('.css'):
                css_files.append(os.path.join(root, file))
            elif file.endswith('.js'):
                js_files.append(os.path.join(root, file))
    
    # البحث عن مجلد الصور
    if os.path.exists(os.path.join(directory, 'images')):
        img_dir = os.path.join(directory, 'images')
    elif os.path.exists(os.path.join(directory, 'img')):
        img_dir = os.path.join(directory, 'img')
    
    return html_files, css_files, js_files, img_dir

@click.command()
@click.option('--html', '-h', help='ملف HTML الرئيسي')
@click.option('--css', '-c', multiple=True, help='ملفات CSS للدمج')
@click.option('--js', '-j', multiple=True, help='ملفات JavaScript للدمج')
@click.option('--img', '-i', help='مجلد الصور للتضمين')
@click.option('--output', '-o', help='ملف الإخراج')
@click.option('--auto', '-a', is_flag=True, help='اكتشاف الملفات تلقائيًا')
def main(html, css, js, img, output, auto):
    """أداة لدمج ملفات HTML و CSS و JavaScript والصور في ملف واحد"""
    print_banner()
    
    current_dir = os.getcwd()
    
    if auto:
        logger.info(f"{Fore.CYAN}الوضع التلقائي: {Fore.WHITE}البحث عن ملفات المشروع في {current_dir}")
        html_files, css_files, js_files, img_dir = find_project_files(current_dir)
        
        if not html_files:
            logger.error(f"{Fore.RED}لم يتم العثور على ملفات HTML في المجلد الحالي")
            sys.exit(1)
        
        # استخدام الملف HTML الأول كملف رئيسي
        html = html_files[0]
        css = css_files
        js = js_files
        img = img_dir
        
        if not output:
            output = os.path.join(current_dir, 'combined.html')
    
    if not html:
        logger.error(f"{Fore.RED}يرجى تحديد ملف HTML باستخدام --html أو تفعيل الوضع التلقائي باستخدام --auto")
        sys.exit(1)
    
    logger.info(f"{Fore.GREEN}جاري معالجة ملف HTML: {Fore.WHITE}{html}")
    
    if css:
        logger.info(f"{Fore.GREEN}ملفات CSS: {Fore.WHITE}{', '.join(css)}")
    
    if js:
        logger.info(f"{Fore.GREEN}ملفات JavaScript: {Fore.WHITE}{', '.join(js)}")
    
    if img:
        logger.info(f"{Fore.GREEN}مجلد الصور: {Fore.WHITE}{img}")
    
    try:
        result = combine_files(html, css, js, img)
        
        if output:
            with open(output, 'w', encoding='utf-8') as f:
                f.write(result)
            logger.info(f"{Fore.GREEN}تم إنشاء الملف المدمج بنجاح: {Fore.WHITE}{output}")
        else:
            print(result)
            
        logger.info(f"{Fore.MAGENTA}اكتملت العملية بنجاح! ✨")
    
    except Exception as e:
        logger.error(f"{Fore.RED}حدث خطأ: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    main()