import requests
from bs4 import BeautifulSoup
import os
from datetime import datetime
import logging
from logging.handlers import RotatingFileHandler
import json
import time
import re
import random
import subprocess

class ArticleCrawler:
    def __init__(self):
        self.base_url = "https://onehu.xyz/archives/"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        self.setup_logging()
        self.template = self.read_template()
        self.cover_images = self.read_cover_images()

    def setup_logging(self):
        if not os.path.exists('logs'):
            os.makedirs('logs')
        
        log_file = 'logs/spiders.log'
        handler = RotatingFileHandler(log_file, maxBytes=1024*1024, backupCount=5)
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[handler]
        )

    def get_total_pages(self, soup):
        # 获取总页数
        pagination = soup.find('span', class_='pagination')
        if pagination:
            last_page = pagination.find_all('a', class_='page-number')[-1]
            return int(last_page.text)
        return 1

    def get_article_content(self, article_url):
        try:
            response = requests.get(article_url, headers=self.headers)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            content = soup.find('div', class_='markdown-body')
            date = soup.find('time').get_text().split()[0].strip()
            if content:
                # 获取所有文本内容，保持原有的段落格式
                text_content = []
                for element in content.children:
                    if element.name in ['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
                        text = element.get_text().strip()
                        if text:
                            text_content.append(text)
                return '\n\n'.join(text_content), date
            return "无法获取文章内容"
        except Exception as e:
            logging.error(f"获取文章内容失败: {str(e)}")
            return "获取文章内容失败"

    def read_template(self):
        """读取模板文件"""
        try:
            with open('template.md', 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            logging.error(f"读取模板文件失败: {str(e)}")
            return ""

    def get_random_cover(self):
        """获取随机封面图片"""
        return random.choice(self.cover_images)

    def save_article(self, title, date, content):
        try:
            # 创建年月目录
            date_match = re.match(r'(\d{4})年(\d{1,2})月(\d{1,2})日', date) # 
            if date_match:
                full_year, month, day = date_match.groups()
                # year = "24"  # 简化年份格式
                year = full_year[2:]
                
                # 修改根目录为 content/posts
                dir_path = os.path.join('../content', 'posts', f"20{year}", f"{month}")
                os.makedirs(dir_path, exist_ok=True)

                # 清理标题中的序号和非法字符
                clean_title = re.sub(r"^\d+\.\s*", '', title)  # 移除开头的数字序号
                safe_title = re.sub(r"\s+", "", clean_title)
                
                # 新的文件名格式：日期-标题.md
                filename = f"{day}-{safe_title}.md"
                file_path = os.path.join(dir_path, filename)
                # 处理文章内容格式
                content = self.format_content(content)
                
                # 准备模板数据
                full_date = f"20{year}-{month}-{day}"
                cover_image = self.get_random_cover()
                
                # 替换模板中的变量
                article_content = self.template.replace("title: ", f"title: {clean_title}")
                article_content = article_content.replace("date: ", f"date: {full_date}")
                article_content = article_content.replace("lastmod: ", f"lastmod: {full_date}")
                article_content = article_content.replace("cover: https://cdn.jsdelivr.net/gh/Pi3-l22/pico_rep/img/c.jpg", 
                                                       f"cover: {cover_image}")
                article_content = article_content.replace("  - https://cdn.jsdelivr.net/gh/Pi3-l22/pico_rep/img/cpp.jpg",
                                                       f"  - {cover_image}")
                
                # 添加文章内容
                article_content += f"\n{content}"
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(article_content)
                
                logging.info(f"保存文章成功: {file_path}")
                return True
            return False
        except Exception as e:
            logging.error(f"保存文章失败: {str(e)}")
            return False

    def format_content(self, content):
        """格式化文章内容"""
        if not content:
            return ""
        
        # 分割成段落并清理
        paragraphs = [p.strip() for p in content.split('\n') if p.strip()]
        
        # 重新组合段落，每段之间只空一行
        formatted_content = '\n\n'.join(paragraphs)
        
        return formatted_content

    def crawl_page(self, page_url):
        try:
            response = requests.get(page_url, headers=self.headers)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 获取文章列表
            articles = soup.find('div', class_='list-group').find_all('a', class_='list-group-item')
            
            for article in articles:
                try:
                    title = article.find('div', class_='list-group-item-title').text.strip()
                    # date = article.find('time').text.strip()
                    article_url = f"https://onehu.xyz{article['href']}"
                    
                    # 获取文章内容
                    content, date = self.get_article_content(article_url)
                    
                    # 保存文章
                    if self.save_article(title, date, content):
                        # 添加延时，避免请求过于频繁
                        time.sleep(1)
                    
                except Exception as e:
                    logging.error(f"处理文章失败: {str(e)}")
                    continue
                    
            return True
            
        except Exception as e:
            logging.error(f"爬取页面失败: {str(e)}")
            return False

    def crawl_all_articles(self):
        try:
            # 获取第一页内容和总页数
            response = requests.get(self.base_url, headers=self.headers)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            total_pages = self.get_total_pages(soup)
            
            logging.info(f"总页数: {total_pages}")
            
            # 爬取第一页
            self.crawl_page(self.base_url)
            
            # 爬取剩余页面
            for page in range(2, total_pages + 1):
                page_url = f"{self.base_url}page/{page}/#board"
                logging.info(f"正在爬取第 {page} 页")
                if not self.crawl_page(page_url):
                    logging.error(f"爬取第 {page} 页失败")
                time.sleep(2)  # 页面间延时
                
        except Exception as e:
            logging.error(f"爬取过程中出现错误: {str(e)}")

    def read_cover_images(self):
        """从cover.txt读取封面图片链接"""
        try:
            with open('cover.txt', 'r', encoding='utf-8') as f:
                # 读取所有行并去除空行和空白字符
                return [line.strip() for line in f.readlines() if line.strip()]
        except Exception as e:
            logging.error(f"读取封面图片列表失败: {str(e)}")
            # 返回一个默认的封面图片列表，以防文件读取失败
            return ["https://raw.githubusercontent.com/Tarikul-Islam-Anik/Animated-Fluent-Emojis/master/Emojis/Smilies/Face%20with%20Crossed-Out%20Eyes.png"]

class GitManager:
    def __init__(self):
        self.logger = logging.getLogger('GitManager')

    def execute_command(self, command):
        """执行 Git 命令并返回结果"""
        try:
            process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                shell=True,
                text=True
            )
            output, error = process.communicate()
            
            if process.returncode != 0:
                self.logger.error(f"Git命令执行失败: {error.strip()}")
                return False
            
            self.logger.info(f"Git命令执行成功: {output.strip()}")
            return True
        except Exception as e:
            self.logger.error(f"执行Git命令时发生错误: {str(e)}")
            return False

    def commit_and_push(self):
        """执行 Git add、commit 和 push 操作"""
        current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) 
        commands = [
            'git add ../',
            f'git commit -m "Python Spiders Commit {current_time}"',
            'git push'
        ]
        
        for command in commands:
            if not self.execute_command(command):
                self.logger.error(f"Git操作失败，停止后续操作")
                return False
        
        return True

if __name__ == "__main__":
    crawler = ArticleCrawler()
    crawler.crawl_all_articles()
    gitmanager = GitManager()
    gitmanager.commit_and_push() 