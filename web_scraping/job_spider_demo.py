# 招聘信息爬虫演示
# 演示基本的爬虫技术和数据处理

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random
import json
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns
import sqlite3
from fake_useragent import UserAgent
import re

class SimpleJobSpider:
    """简化的招聘信息爬虫演示"""

    def __init__(self):
        self.ua = UserAgent()
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': self.ua.random,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        })

        # 初始化数据库
        self.init_database()

    def init_database(self):
        """初始化数据库"""
        self.conn = sqlite3.connect('job_demo.db')
        cursor = self.conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS demo_jobs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                company TEXT,
                salary TEXT,
                location TEXT,
                source TEXT,
                crawl_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        self.conn.commit()

    def crawl_zhipin_demo(self, keyword="Python", pages=1):
        """演示爬取Boss直聘（注意：实际使用时需遵守网站规则）"""
        print(f"🔍 演示爬取Boss直聘 - 关键词: {keyword}")

        jobs = []

        for page in range(1, pages + 1):
            try:
                # 注意：这是演示URL，实际爬取时需要处理动态加载和反爬虫
                url = f"https://www.zhipin.com/web/geek/job?query={keyword}&page={page}"
                print(f"请求页面: {url}")

                # 由于Boss直聘有反爬虫措施，这里只做请求演示
                response = self.session.get(url, timeout=10)

                if response.status_code == 200:
                    print(f"✅ 页面 {page} 请求成功 (状态码: {response.status_code})")

                    # 解析HTML（实际项目中需要处理动态内容）
                    soup = BeautifulSoup(response.text, 'html.parser')

                    # 这里是演示数据，实际爬取需要根据页面结构调整选择器
                    demo_jobs = [
                        {
                            'title': f'Python开发工程师-{page}-{i+1}',
                            'company': f'科技公司{i+1}',
                            'salary': f'{random.randint(15, 50)}k-{random.randint(20, 80)}k',
                            'location': random.choice(['北京', '上海', '深圳', '杭州', '广州']),
                            'source': 'Boss直聘(演示)'
                        } for i in range(5)
                    ]

                    jobs.extend(demo_jobs)

                else:
                    print(f"❌ 页面 {page} 请求失败 (状态码: {response.status_code})")

            except Exception as e:
                print(f"❌ 爬取页面 {page} 时出错: {e}")

            # 延迟避免请求过快
            time.sleep(random.uniform(1, 3))

        return jobs

    def crawl_lagou_demo(self, keyword="Python", pages=1):
        """演示爬取拉勾网"""
        print(f"🔍 演示爬取拉勾网 - 关键词: {keyword}")

        jobs = []

        for page in range(1, pages + 1):
            try:
                url = f"https://www.lagou.com/wn/jobs?pn={page}&kd={keyword}"
                print(f"请求页面: {url}")

                response = self.session.get(url, timeout=10)

                if response.status_code == 200:
                    print(f"✅ 页面 {page} 请求成功 (状态码: {response.status_code})")

                    # 演示数据
                    demo_jobs = [
                        {
                            'title': f'后端开发工程师-{page}-{i+1}',
                            'company': f'互联网公司{i+1}',
                            'salary': f'{random.randint(20, 60)}k-{random.randint(30, 100)}k',
                            'location': random.choice(['北京', '上海', '深圳', '杭州', '成都']),
                            'source': '拉勾网(演示)'
                        } for i in range(5)
                    ]

                    jobs.extend(demo_jobs)

                else:
                    print(f"❌ 页面 {page} 请求失败 (状态码: {response.status_code})")

            except Exception as e:
                print(f"❌ 爬取页面 {page} 时出错: {e}")

            time.sleep(random.uniform(1, 3))

        return jobs

    def save_jobs_to_db(self, jobs):
        """保存职位到数据库"""
        cursor = self.conn.cursor()

        for job in jobs:
            try:
                cursor.execute('''
                    INSERT INTO demo_jobs (title, company, salary, location, source)
                    VALUES (?, ?, ?, ?, ?)
                ''', (job['title'], job['company'], job['salary'], job['location'], job['source']))

            except Exception as e:
                print(f"保存职位失败: {e}")

        self.conn.commit()
        print(f"✅ 已保存 {len(jobs)} 个职位到数据库")

    def analyze_and_visualize(self):
        """分析数据并可视化"""
        # 从数据库读取数据
        df = pd.read_sql_query("SELECT * FROM demo_jobs", self.conn)

        if df.empty:
            print("❌ 没有数据可分析")
            return

        print("\n📊 数据分析:")
        print(f"总职位数: {len(df)}")
        print(f"独特公司数: {df['company'].nunique()}")
        print(f"数据源分布: {df['source'].value_counts().to_dict()}")

        # 薪资分析（简化版）
        def extract_salary_range(salary_str):
            """提取薪资范围"""
            numbers = re.findall(r'\d+', salary_str)
            if len(numbers) >= 2:
                return (int(numbers[0]) + int(numbers[1])) / 2  # 取平均值
            return 0

        df['avg_salary'] = df['salary'].apply(extract_salary_range)

        # 可视化
        plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS']
        plt.rcParams['axes.unicode_minus'] = False

        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        fig.suptitle('招聘数据分析演示', fontsize=16)

        # 1. 数据源分布
        source_counts = df['source'].value_counts()
        axes[0, 0].pie(source_counts.values, labels=source_counts.index, autopct='%1.1f%%')
        axes[0, 0].set_title('数据源分布')

        # 2. 薪资分布
        if df['avg_salary'].max() > 0:
            axes[0, 1].hist(df['avg_salary'], bins=10, edgecolor='black')
            axes[0, 1].set_title('薪资分布')
            axes[0, 1].set_xlabel('平均薪资(k)')
            axes[0, 1].set_ylabel('职位数量')

        # 3. 工作地点分布
        location_counts = df['location'].value_counts()
        axes[1, 0].bar(location_counts.index, location_counts.values)
        axes[1, 0].set_title('工作地点分布')
        axes[1, 0].tick_params(axis='x', rotation=45)

        # 4. 公司职位数量
        company_counts = df['company'].value_counts().head(10)
        axes[1, 1].barh(company_counts.index, company_counts.values)
        axes[1, 1].set_title('公司职位数量TOP10')

        plt.tight_layout()
        plt.savefig('job_analysis_demo.png', dpi=300, bbox_inches='tight')
        plt.show()

        # 生成简单报告
        report = f"""
# 招聘数据分析报告（演示）
生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 基本统计
- 总职位数: {len(df)}
- 独特公司数: {df['company'].nunique()}
- 平均薪资: {df['avg_salary'].mean():.1f}k

## 数据源分布
{source_counts.to_string()}

## 热门城市
{location_counts.head(5).to_string()}
"""
        with open('job_report_demo.md', 'w', encoding='utf-8') as f:
            f.write(report)

        print("✅ 分析完成！生成文件：job_analysis_demo.png, job_report_demo.md")

    def close(self):
        """关闭数据库连接"""
        if self.conn:
            self.conn.close()

def main():
    """主函数演示"""
    print("🎯 招聘信息爬虫演示系统")
    print("=" * 50)
    print("⚠️  注意：本演示仅用于学习目的")
    print("⚠️  实际爬取时请遵守网站robots.txt和使用条款")
    print("⚠️  建议使用官方API或合作接口")
    print("=" * 50)

    spider = SimpleJobSpider()

    try:
        # 1. 爬取Boss直聘演示数据
        print("\n1️⃣ 爬取Boss直聘演示数据...")
        boss_jobs = spider.crawl_zhipin_demo("Python", pages=2)

        # 2. 爬取拉勾网演示数据
        print("\n2️⃣ 爬取拉勾网演示数据...")
        lagou_jobs = spider.crawl_lagou_demo("Python", pages=2)

        # 3. 合并数据
        all_jobs = boss_jobs + lagou_jobs
        print(f"\n📊 共获取 {len(all_jobs)} 个演示职位")

        # 4. 保存到数据库
        print("\n3️⃣ 保存数据到数据库...")
        spider.save_jobs_to_db(all_jobs)

        # 5. 分析和可视化
        print("\n4️⃣ 分析数据并生成可视化...")
        spider.analyze_and_visualize()

        print("\n🎉 演示完成！")
        print("📁 生成的文件:")
        print("- job_demo.db: 演示数据库")
        print("- job_analysis_demo.png: 数据可视化图表")
        print("- job_report_demo.md: 分析报告")

    except Exception as e:
        print(f"❌ 演示过程中出错: {e}")
    finally:
        spider.close()

if __name__ == "__main__":
    main()
