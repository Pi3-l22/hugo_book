from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from crawler import ArticleCrawler, GitManager
import logging
import random
import json
import os
from datetime import datetime, timedelta
import requests
from bs4 import BeautifulSoup

class CrawlerScheduler:
    def __init__(self):
        self.crawler = ArticleCrawler()
        self.scheduler = BlockingScheduler()
        self.last_count_file = "last_article_count.json"
        self.setup_logging()

    def setup_logging(self):
        if not os.path.exists('logs'):
            os.makedirs('logs')
        
        log_file = 'logs/scheduler.log'
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )

    def get_current_article_count(self):
        """获取网站当前的文章总数"""
        try:
            response = requests.get(self.crawler.base_url, headers=self.crawler.headers)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            
            count_text = soup.find('div', class_='list-group').find('p', class_='h4').text
            count = int(count_text.split()[1])  # "共计 6073 篇文章" -> 6073
            return count
        except Exception as e:
            logging.error(f"获取文章数量失败: {str(e)}")
            return None

    def get_last_article_count(self):
        """获取上次记录的文章数量"""
        try:
            if os.path.exists(self.last_count_file):
                with open(self.last_count_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return data.get('count', 0)
            return 0
        except Exception as e:
            logging.error(f"读取上次文章数量失败: {str(e)}")
            return 0

    def save_article_count(self, count):
        """保存当前文章数量"""
        try:
            with open(self.last_count_file, 'w', encoding='utf-8') as f:
                json.dump({'count': count, 'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')}, f)
        except Exception as e:
            logging.error(f"保存文章数量失败: {str(e)}")

    def crawl_job(self):
        """爬虫任务"""
        try:
            current_count = self.get_current_article_count()
            last_count = self.get_last_article_count()

            if current_count is None:
                logging.error("无法获取当前文章数量，跳过本次爬取")
                return

            if current_count > last_count:
                logging.info(f"检测到新文章，从 {last_count} 增加到 {current_count}")
                # 修改为只爬取新文章
                if self.crawler.crawl_new_articles(last_count, current_count):
                    self.save_article_count(current_count)
                    
                    # 添加 Git 提交操作
                    git_manager = GitManager()
                    if git_manager.commit_and_push():
                        logging.info("Git提交成功")
                    else:
                        logging.error("Git提交失败")
                else:
                    logging.error("爬取新文章失败")
            else:
                logging.info(f"未检测到新文章，当前文章数: {current_count}")

        except Exception as e:
            logging.error(f"爬虫任务执行失败: {str(e)}")

    def random_time_trigger(self, base_hour):
        """生成随机时间触发器"""
        # 在基准时间前后30分钟内随机
        minutes = random.randint(-30, 30)
        return CronTrigger(
            hour=base_hour,
            minute=30 + minutes,  # 基准分钟数30，加上随机偏移
            jitter=300  # 添加额外的5分钟随机偏移
        )

    def start(self):
        """启动定时任务"""
        # 添加两个定时任务，分别在0点和12点前后运行
        self.scheduler.add_job(
            self.crawl_job,
            trigger=self.random_time_trigger(6),
            id='crawler_midnight'
        )
        self.scheduler.add_job(
            self.crawl_job,
            trigger=self.random_time_trigger(18),
            id='crawler_noon'
        )

        logging.info("定时任务已启动")
        try:
            self.scheduler.start()
        except (KeyboardInterrupt, SystemExit):
            logging.info("定时任务已停止")

if __name__ == '__main__':
    scheduler = CrawlerScheduler()
    scheduler.start() 
    # count = scheduler.get_current_article_count()
    # scheduler.save_article_count(count)