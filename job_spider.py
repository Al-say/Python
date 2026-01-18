# 现代化招聘信息爬虫系统
# 使用异步技术、反爬虫策略和数据可视化

import asyncio
import aiohttp
import json
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import re
import time
import random
from urllib.parse import urljoin, urlparse
import matplotlib.pyplot as plt
import seaborn as sns
from collections import defaultdict
import sqlite3
from typing import List, Dict, Optional
import logging
from fake_useragent import UserAgent
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class JobSpider:
    """现代化招聘信息爬虫"""

    def __init__(self, db_path='job_data.db'):
        self.db_path = db_path
        self.ua = UserAgent()
        self.session = None
        self.driver = None
        self.init_database()

        # 反爬虫策略
        self.request_delay = (1, 3)  # 请求间隔1-3秒
        self.max_retries = 3
        self.timeout = 30

        # 目标网站配置
        self.sources = {
            'lagou': {
                'name': '拉勾网',
                'base_url': 'https://www.lagou.com',
                'search_url': 'https://www.lagou.com/wn/jobs?pn={page}&kd={keyword}',
                'parser': self.parse_lagou
            },
            'boss': {
                'name': 'Boss直聘',
                'base_url': 'https://www.zhipin.com',
                'search_url': 'https://www.zhipin.com/web/geek/job?query={keyword}&page={page}',
                'parser': self.parse_boss,
                'use_selenium': True
            },
            'bilibili': {
                'name': 'Bilibili招聘',
                'base_url': 'https://jobs.bilibili.com',
                'search_url': 'https://jobs.bilibili.com/search?keyword={keyword}&page={page}',
                'parser': self.parse_bilibili
            }
        }

    def init_database(self):
        """初始化数据库"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # 创建招聘信息表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS jobs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                job_id TEXT UNIQUE,
                title TEXT NOT NULL,
                company TEXT NOT NULL,
                salary TEXT,
                location TEXT,
                experience TEXT,
                education TEXT,
                description TEXT,
                tags TEXT,  -- JSON格式存储标签
                source TEXT,
                url TEXT,
                publish_time TEXT,
                crawl_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                status TEXT DEFAULT 'active'
            )
        ''')

        # 创建公司信息表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS companies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE,
                industry TEXT,
                size TEXT,
                description TEXT,
                website TEXT,
                logo_url TEXT,
                update_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # 创建搜索关键词表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS search_keywords (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                keyword TEXT UNIQUE,
                search_count INTEGER DEFAULT 0,
                last_search TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        conn.commit()
        conn.close()
        logger.info("✅ 数据库初始化完成")

    def init_session(self):
        """初始化异步会话"""
        if not self.session:
            self.session = aiohttp.ClientSession(
                headers={
                    'User-Agent': self.ua.random,
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
                    'Accept-Encoding': 'gzip, deflate, br',
                    'Connection': 'keep-alive',
                    'Upgrade-Insecure-Requests': '1',
                }
            )

    def init_selenium_driver(self):
        """初始化Selenium浏览器"""
        if not self.driver:
            options = Options()
            options.add_argument('--headless')  # 无头模式
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--disable-blink-features=AutomationControlled')
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option('useAutomationExtension', False)
            options.add_argument(f'--user-agent={self.ua.random}')

            self.driver = webdriver.Chrome(options=options)
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

    async def close(self):
        """关闭资源"""
        if self.session:
            await self.session.close()
        if self.driver:
            self.driver.quit()

    def save_job(self, job_data: Dict):
        """保存招聘信息到数据库"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        try:
            cursor.execute('''
                INSERT OR REPLACE INTO jobs
                (job_id, title, company, salary, location, experience, education,
                 description, tags, source, url, publish_time)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                job_data.get('job_id'),
                job_data.get('title'),
                job_data.get('company'),
                job_data.get('salary'),
                job_data.get('location'),
                job_data.get('experience'),
                job_data.get('education'),
                job_data.get('description'),
                json.dumps(job_data.get('tags', [])),
                job_data.get('source'),
                job_data.get('url'),
                job_data.get('publish_time')
            ))
            conn.commit()
            logger.info(f"✅ 保存职位: {job_data.get('title')} - {job_data.get('company')}")

        except Exception as e:
            logger.error(f"❌ 保存职位失败: {e}")
        finally:
            conn.close()

    async def fetch_page(self, url: str, use_selenium: bool = False) -> Optional[str]:
        """获取页面内容"""
        for attempt in range(self.max_retries):
            try:
                if use_selenium:
                    if not self.driver:
                        self.init_selenium_driver()
                    self.driver.get(url)
                    WebDriverWait(self.driver, 10).until(
                        EC.presence_of_element_located((By.TAG_NAME, "body"))
                    )
                    return self.driver.page_source
                else:
                    if not self.session:
                        self.init_session()
                    async with self.session.get(url, timeout=self.timeout) as response:
                        if response.status == 200:
                            return await response.text()
                        else:
                            logger.warning(f"请求失败: {url} - 状态码: {response.status}")

            except Exception as e:
                logger.warning(f"请求失败 (尝试 {attempt + 1}/{self.max_retries}): {e}")

            # 随机延迟
            await asyncio.sleep(random.uniform(*self.request_delay))

        return None

    def parse_lagou(self, html: str, source_config: Dict) -> List[Dict]:
        """解析拉勾网招聘信息"""
        soup = BeautifulSoup(html, 'html.parser')
        jobs = []

        # 拉勾网的职位列表选择器（可能需要根据实际页面调整）
        job_items = soup.select('.job-list .job-item') or soup.select('[data-jobid]')

        for item in job_items[:10]:  # 限制数量避免被限制
            try:
                job = {
                    'job_id': f"lagou_{item.get('data-jobid', str(hash(str(item))))}",
                    'title': item.select_one('.job-name, .position-link h3').text.strip() if item.select_one('.job-name, .position-link h3') else '',
                    'company': item.select_one('.company-name, .company').text.strip() if item.select_one('.company-name, .company') else '',
                    'salary': item.select_one('.salary, .money').text.strip() if item.select_one('.salary, .money') else '',
                    'location': item.select_one('.job-area, .area').text.strip() if item.select_one('.job-area, .area') else '',
                    'experience': item.select_one('.experience').text.strip() if item.select_one('.experience') else '',
                    'education': item.select_one('.education').text.strip() if item.select_one('.education') else '',
                    'description': item.select_one('.job-desc, .description').text.strip() if item.select_one('.job-desc, .description') else '',
                    'tags': [tag.text.strip() for tag in item.select('.tags span, .labels span')],
                    'source': '拉勾网',
                    'url': urljoin(source_config['base_url'], item.select_one('a')['href']) if item.select_one('a') else '',
                    'publish_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }
                if job['title'] and job['company']:
                    jobs.append(job)
            except Exception as e:
                logger.warning(f"解析拉勾网职位失败: {e}")
                continue

        return jobs

    def parse_boss(self, html: str, source_config: Dict) -> List[Dict]:
        """解析Boss直聘招聘信息"""
        soup = BeautifulSoup(html, 'html.parser')
        jobs = []

        # Boss直聘的职位列表选择器
        job_items = soup.select('.job-card-wrapper, .job-list-item')

        for item in job_items[:10]:
            try:
                job = {
                    'job_id': f"boss_{item.get('data-jobid', str(hash(str(item))))}",
                    'title': item.select_one('.job-name, .job-title').text.strip() if item.select_one('.job-name, .job-title') else '',
                    'company': item.select_one('.company-name, .company-text').text.strip() if item.select_one('.company-name, .company-text') else '',
                    'salary': item.select_one('.salary, .money').text.strip() if item.select_one('.salary, .money') else '',
                    'location': item.select_one('.job-area, .area').text.strip() if item.select_one('.job-area, .area') else '',
                    'experience': item.select_one('.job-experience, .experience').text.strip() if item.select_one('.job-experience, .experience') else '',
                    'education': item.select_one('.job-education, .education').text.strip() if item.select_one('.job-education, .education') else '',
                    'description': item.select_one('.job-desc, .description').text.strip() if item.select_one('.job-desc, .description') else '',
                    'tags': [tag.text.strip() for tag in item.select('.tag, .labels span')],
                    'source': 'Boss直聘',
                    'url': urljoin(source_config['base_url'], item.select_one('a')['href']) if item.select_one('a') else '',
                    'publish_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }
                if job['title'] and job['company']:
                    jobs.append(job)
            except Exception as e:
                logger.warning(f"解析Boss直聘职位失败: {e}")
                continue

        return jobs

    def parse_bilibili(self, html: str, source_config: Dict) -> List[Dict]:
        """解析Bilibili招聘信息"""
        soup = BeautifulSoup(html, 'html.parser')
        jobs = []

        # Bilibili招聘的职位列表选择器
        job_items = soup.select('.job-item, .position-item')

        for item in job_items[:10]:
            try:
                job = {
                    'job_id': f"bilibili_{item.get('data-jobid', str(hash(str(item))))}",
                    'title': item.select_one('.job-title, .position-title').text.strip() if item.select_one('.job-title, .position-title') else '',
                    'company': '哔哩哔哩',  # B站招聘通常是内部招聘
                    'salary': item.select_one('.salary, .money').text.strip() if item.select_one('.salary, .money') else '',
                    'location': item.select_one('.location, .area').text.strip() if item.select_one('.location, .area') else '',
                    'experience': item.select_one('.experience').text.strip() if item.select_one('.experience') else '',
                    'education': item.select_one('.education').text.strip() if item.select_one('.education') else '',
                    'description': item.select_one('.description, .job-desc').text.strip() if item.select_one('.description, .job-desc') else '',
                    'tags': [tag.text.strip() for tag in item.select('.tag, .label')],
                    'source': 'Bilibili招聘',
                    'url': urljoin(source_config['base_url'], item.select_one('a')['href']) if item.select_one('a') else '',
                    'publish_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }
                if job['title']:
                    jobs.append(job)
            except Exception as e:
                logger.warning(f"解析Bilibili招聘职位失败: {e}")
                continue

        return jobs

    async def crawl_source(self, source_name: str, keyword: str, max_pages: int = 3) -> List[Dict]:
        """爬取单个数据源"""
        source_config = self.sources.get(source_name)
        if not source_config:
            logger.error(f"不支持的数据源: {source_name}")
            return []

        all_jobs = []
        logger.info(f"开始爬取 {source_config['name']} - 关键词: {keyword}")

        for page in range(1, max_pages + 1):
            try:
                url = source_config['search_url'].format(keyword=keyword, page=page)
                logger.info(f"爬取第 {page} 页: {url}")

                html = await self.fetch_page(url, source_config.get('use_selenium', False))
                if not html:
                    logger.warning(f"获取页面失败: {url}")
                    continue

                jobs = source_config['parser'](html, source_config)
                all_jobs.extend(jobs)

                logger.info(f"第 {page} 页获取到 {len(jobs)} 个职位")

                # 页面间延迟
                await asyncio.sleep(random.uniform(2, 5))

            except Exception as e:
                logger.error(f"爬取第 {page} 页失败: {e}")
                continue

        return all_jobs

    async def crawl_all_sources(self, keyword: str, max_pages: int = 2) -> List[Dict]:
        """并发爬取所有数据源"""
        logger.info(f"开始并发爬取所有数据源 - 关键词: {keyword}")

        tasks = []
        for source_name in self.sources.keys():
            task = self.crawl_source(source_name, keyword, max_pages)
            tasks.append(task)

        results = await asyncio.gather(*tasks, return_exceptions=True)

        all_jobs = []
        for i, result in enumerate(results):
            source_name = list(self.sources.keys())[i]
            if isinstance(result, Exception):
                logger.error(f"爬取 {source_name} 失败: {result}")
            else:
                all_jobs.extend(result)
                logger.info(f"{source_name} 共获取 {len(result)} 个职位")

        return all_jobs

    def analyze_jobs(self, jobs: List[Dict]) -> Dict:
        """分析招聘数据"""
        if not jobs:
            return {}

        df = pd.DataFrame(jobs)

        analysis = {
            'total_jobs': len(df),
            'unique_companies': df['company'].nunique(),
            'sources': df['source'].value_counts().to_dict(),
            'locations': df['location'].value_counts().head(10).to_dict(),
            'salary_ranges': self.analyze_salary(df),
            'experience_distribution': df['experience'].value_counts().to_dict() if 'experience' in df.columns else {},
            'education_distribution': df['education'].value_counts().to_dict() if 'education' in df.columns else {},
            'top_companies': df['company'].value_counts().head(10).to_dict(),
            'common_tags': self.analyze_tags(df)
        }

        return analysis

    def analyze_salary(self, df: pd.DataFrame) -> Dict:
        """分析薪资分布"""
        salary_ranges = defaultdict(int)

        for salary in df['salary'].dropna():
            # 简单的薪资范围识别（可以根据实际数据调整）
            if 'k' in salary.lower() or '千' in salary:
                if '-' in salary:
                    parts = salary.replace('k', '').replace('千', '').split('-')
                    try:
                        min_salary = float(parts[0].strip())
                        max_salary = float(parts[1].strip())
                        if max_salary <= 20:
                            salary_ranges['0-20k'] += 1
                        elif max_salary <= 50:
                            salary_ranges['20-50k'] += 1
                        else:
                            salary_ranges['50k+'] += 1
                    except:
                        salary_ranges['未知'] += 1
                else:
                    salary_ranges['面议/未知'] += 1
            else:
                salary_ranges['面议/未知'] += 1

        return dict(salary_ranges)

    def analyze_tags(self, df: pd.DataFrame) -> Dict:
        """分析职位标签"""
        all_tags = []
        for tags in df['tags'].dropna():
            if isinstance(tags, str):
                try:
                    tag_list = json.loads(tags)
                    all_tags.extend(tag_list)
                except:
                    continue
            elif isinstance(tags, list):
                all_tags.extend(tags)

        tag_counts = pd.Series(all_tags).value_counts().head(20)
        return tag_counts.to_dict()

    def visualize_analysis(self, analysis: Dict, keyword: str):
        """可视化分析结果"""
        if not analysis:
            return

        # 设置中文字体
        plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS', 'DejaVu Sans']
        plt.rcParams['axes.unicode_minus'] = False

        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        fig.suptitle(f'招聘数据分析 - 关键词: {keyword}', fontsize=16)

        # 1. 数据源分布
        if 'sources' in analysis:
            sources = analysis['sources']
            axes[0, 0].pie(sources.values(), labels=sources.keys(), autopct='%1.1f%%')
            axes[0, 0].set_title('数据源分布')

        # 2. 薪资分布
        if 'salary_ranges' in analysis:
            salary_data = analysis['salary_ranges']
            axes[0, 1].bar(salary_data.keys(), salary_data.values())
            axes[0, 1].set_title('薪资分布')
            axes[0, 1].tick_params(axis='x', rotation=45)

        # 3. 工作地点分布
        if 'locations' in analysis:
            locations = analysis['locations']
            axes[1, 0].bar(locations.keys(), locations.values())
            axes[1, 0].set_title('工作地点分布')
            axes[1, 0].tick_params(axis='x', rotation=45)

        # 4. 热门公司
        if 'top_companies' in analysis:
            companies = analysis['top_companies']
            axes[1, 1].barh(list(companies.keys()), list(companies.values()))
            axes[1, 1].set_title('热门公司')

        plt.tight_layout()
        plt.savefig(f'job_analysis_{keyword}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.png', dpi=300, bbox_inches='tight')
        plt.show()

        # 生成分析报告
        self.generate_report(analysis, keyword)

    def generate_report(self, analysis: Dict, keyword: str):
        """生成分析报告"""
        report = f"""
# 招聘数据分析报告
## 搜索关键词: {keyword}
## 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

### 📊 基本统计
- 总职位数: {analysis.get('total_jobs', 0)}
- 独特公司数: {analysis.get('unique_companies', 0)}

### 📍 数据源分布
"""
        if 'sources' in analysis:
            for source, count in analysis['sources'].items():
                report += f"- {source}: {count} 个职位\n"

        report += "\n### 💰 薪资分布\n"
        if 'salary_ranges' in analysis:
            for salary_range, count in analysis['salary_ranges'].items():
                report += f"- {salary_range}: {count} 个职位\n"

        report += "\n### 🏢 热门公司 TOP 10\n"
        if 'top_companies' in analysis:
            for i, (company, count) in enumerate(analysis['top_companies'].items(), 1):
                report += f"{i}. {company}: {count} 个职位\n"

        report += "\n### 📍 热门工作地点 TOP 10\n"
        if 'locations' in analysis:
            for i, (location, count) in enumerate(analysis['locations'].items(), 1):
                report += f"{i}. {location}: {count} 个职位\n"

        # 保存报告
        filename = f'job_report_{keyword}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.md'
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(report)

        logger.info(f"✅ 分析报告已保存: {filename}")

    async def run_crawler(self, keyword: str, max_pages: int = 2):
        """运行完整的爬虫流程"""
        logger.info(f"🚀 开始爬取招聘信息 - 关键词: {keyword}")

        try:
            # 1. 并发爬取所有数据源
            jobs = await self.crawl_all_sources(keyword, max_pages)

            # 2. 保存到数据库
            for job in jobs:
                self.save_job(job)

            # 3. 分析数据
            analysis = self.analyze_jobs(jobs)

            # 4. 可视化分析结果
            if analysis:
                self.visualize_analysis(analysis, keyword)

            logger.info(f"✅ 爬取完成! 共获取 {len(jobs)} 个职位")

        except Exception as e:
            logger.error(f"❌ 爬取过程出错: {e}")
        finally:
            await self.close()


async def main():
    """主函数"""
    print("🎯 现代化招聘信息爬虫系统")
    print("=" * 50)

    # 初始化爬虫
    spider = JobSpider()

    # 设置搜索关键词
    keywords = ["Python工程师", "数据分析师", "机器学习工程师"]

    for keyword in keywords:
        print(f"\n🔍 开始搜索: {keyword}")
        await spider.run_crawler(keyword, max_pages=2)

        # 关键词间间隔
        await asyncio.sleep(5)

    print("\n🎉 所有关键词搜索完成!")
    print("📁 生成的文件:")
    print("- job_data.db: 招聘数据数据库")
    print("- job_analysis_*.png: 数据可视化图表")
    print("- job_report_*.md: 详细分析报告")


if __name__ == "__main__":
    asyncio.run(main())
