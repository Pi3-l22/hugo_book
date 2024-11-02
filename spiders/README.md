# 定时爬虫项目说明文档

## 项目概述

这是一个用于爬取目标网站信息的自动化爬虫程序。程序主要包含两个核心组件：

1. 文章爬虫（ArticleCrawler）
2. 定时调度器（CrawlerScheduler）

该项目可以定期检查目标网站信息的更新，自动爬取新发布的文章，并将其保存为 Markdown 格式。最后使用 Git 将代码上传至仓库中，使用 GitHub Action + Hugo 自动构建静态网站并发布，可以随时在个人网站上浏览最新爬取的信息。

## 核心功能

### 文章爬虫 (crawler.py)

#### 主要功能：
- 爬取目标网站文章内容
- 格式化文章内容
- 保存为 Markdown 文件
- 自动管理文件目录结构
- Git 自动提交更新

#### 关键类和方法：

**ArticleCrawler 类**：

```python
class ArticleCrawler:
    def __init__(self):
        self.base_url = "https://example.com/"
        # 初始化配置...
```
主要方法：
- `get_article_content()`: 获取文章内容
- `save_article()`: 保存文章到指定目录
- `crawl_new_articles()`: 只爬取新增的文章
- `format_content()`: 格式化文章内容

**GitManager 类**：

```python
class GitManager:
    def __init__(self):
        self.logger = logging.getLogger('GitManager')
```

负责自动执行 Git 操作，包括 add、commit 和 push。

### 定时调度器 (scheduler.py)

#### 主要功能：
- 定时检查网站更新
- 智能判断新文章
- 自动触发爬虫任务
- 记录文章数量变化

#### 关键类和方法：

**CrawlerScheduler 类**：

```python
class CrawlerScheduler:
    def __init__(self):
        self.crawler = ArticleCrawler()
        self.scheduler = BlockingScheduler()
```

主要方法：
- `get_current_article_count()`: 获取当前文章总数
- `crawl_job()`: 执行爬虫任务
- `random_time_trigger()`: 生成随机执行时间
- `start()`: 启动定时任务

## 项目特点

1. **智能增量爬取**
   - 只爬取新增文章，避免重复爬取
   - 通过比对文章数量判断更新

2. **随机化执行时间**
   - 避免固定时间爬取
   - 在指定时间段内随机执行

3. **完善的日志系统**
   - 记录爬虫运行状态
   - 错误追踪和调试

4. **自动化 Git 管理**
   - 自动提交更新
   - 保持仓库同步

## 使用说明

### 环境要求
1. python 3.x
2. requests
3. beautifulsoup4
4. apscheduler

### 配置文件
需要准备以下文件：
- `template.md`: 文章模板文件
- `cover.txt`: 封面图片链接列表
- `logs/`: 日志目录

### 运行方式

直接运行爬虫，爬取目标网站所有指定信息：
python crawler.py

启动定时任务，定时爬取更新的信息：
python scheduler.py

## 项目结构

```shell
project/
├── crawler.py      # 爬虫核心代码
├── scheduler.py    # 定时调度器
├── template.md     # 文章模板
├── cover.txt       # 封面图片列表
└── logs/           # 日志目录
    ├── spiders.log
    └── scheduler.log
```
## 注意事项

1. 请合理设置爬取间隔，避免对目标网站造成压力
2. 确保 Git 配置正确，以便自动提交
3. 定期检查日志文件，及时处理异常情况
4. 建议定期备份已爬取的文章

## 扩展建议

1. 添加代理池支持
2. 实现断点续爬功能
3. 添加文章内容查重
4. 增加更多的异常处理机制
5. 添加邮件通知功能
