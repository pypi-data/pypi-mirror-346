# htvanila/utils.py
import os
import re
import base64
import logging
import mimetypes
from colorama import Fore, Style, init

init(autoreset=True)  # تهيئة colorama

def setup_logging():
    """إعداد التسجيل مع ألوان"""
    logger = logging.getLogger('HtVanila')
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        
        formatter = logging.Formatter(
            f'{Fore.CYAN}[%(asctime)s]{Style.RESET_ALL} {Fore.GREEN}%(levelname)s:{Style.RESET_ALL} %(message)s',
            datefmt='%H:%M:%S'
        )
        
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        
        logger.addHandler(console_handler)
    
    return logger

def get_file_content(file_path):
    """قراءة محتوى الملف مع معالجة الأخطاء"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except UnicodeDecodeError:
        # محاولة بترميز آخر
        with open(file_path, 'r', encoding='latin-1') as f:
            return f.read()
    except Exception as e:
        logger = setup_logging()
        logger.error(f"خطأ في قراءة الملف {file_path}: {str(e)}")
        return ""

def is_url(path):
    """التحقق مما إذا كان المسار عبارة عن URL"""
    return path.startswith(('http://', 'https://', '//'))

def file_to_base64(file_path):
    """تحويل ملف إلى تشفير base64"""
    with open(file_path, 'rb') as f:
        return base64.b64encode(f.read()).decode('utf-8')

def print_banner():
    """عرض شعار البرنامج بألوان جميلة"""
    banner = f"""
{Fore.MAGENTA}╭───────────────────────────────────────────╮
{Fore.MAGENTA}│                                           │
{Fore.MAGENTA}│ {Fore.YELLOW}  _   _ _{Fore.GREEN}__     __   {Fore.CYAN}_      {Fore.BLUE} _  _      {Fore.MAGENTA}│
{Fore.MAGENTA}│ {Fore.YELLOW} | | | | {Fore.GREEN}\ \   / /  {Fore.CYAN}/ \    {Fore.BLUE}| \| |     {Fore.MAGENTA}│
{Fore.MAGENTA}│ {Fore.YELLOW} | |_| |  {Fore.GREEN}\ \ / /  {Fore.CYAN}/ _ \   {Fore.BLUE}| .` |     {Fore.MAGENTA}│
{Fore.MAGENTA}│ {Fore.YELLOW} |  _  |   {Fore.GREEN}\ V /  {Fore.CYAN}/ ___ \  {Fore.BLUE}| |\ |     {Fore.MAGENTA}│
{Fore.MAGENTA}│ {Fore.YELLOW} |_| |_|    {Fore.GREEN}\_/  {Fore.CYAN}/_/   \_\ {Fore.BLUE}|_| \_|    {Fore.MAGENTA}│
{Fore.MAGENTA}│                                           │
{Fore.MAGENTA}│ {Fore.CYAN}HTML, CSS, JS & Images Combiner Tool {Fore.MAGENTA}│
{Fore.MAGENTA}│ {Fore.WHITE}v0.1.0                               {Fore.MAGENTA}│
{Fore.MAGENTA}╰───────────────────────────────────────────╯
    """
    print(banner)