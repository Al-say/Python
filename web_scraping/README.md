# Web Scraping - 网络爬虫模块

本文件夹包含完整的网络爬虫功能实现，专注于招聘信息的自动化采集和分析。

## 📁 文件结构

```
web_scraping/
├── job_spider.py              # 完整版现代化爬虫（生产环境）
├── job_spider_demo.py         # 演示版爬虫（学习推荐）
├── job_demo.db               # SQLite数据库（爬取数据存储）
├── job_analysis_demo.png     # 数据分析可视化图表
├── job_report_demo.md        # 自动生成的分析报告
└── JOB_SPIDER_README.md      # 详细使用说明
```

## 🚀 核心功能

### 1. 招聘信息爬取
- **Boss直聘**: 国内领先招聘平台
- **拉勾网**: 互联网行业招聘
- **Bilibili招聘**: B站内部招聘

### 2. 技术特性
- **异步爬取**: 高并发数据采集
- **反爬虫策略**: 智能请求控制
- **数据存储**: SQLite数据库持久化
- **数据分析**: 自动生成可视化报告

### 3. 数据分析
- 薪资分布分析
- 职位要求统计
- 公司规模分析
- 工作经验要求分析

## 🛠️ 快速开始

### 演示版本（推荐学习）
```bash
cd web_scraping
python job_spider_demo.py
```

### 完整版本（生产环境）
```bash
cd web_scraping
python job_spider.py
```

## 📊 输出文件

运行爬虫后会生成：
- `job_demo.db`: 包含所有爬取的招聘信息
- `job_analysis_demo.png`: 数据可视化图表
- `job_report_demo.md`: 详细分析报告

## 🔗 相关模块

- `../database_connection.py`: 通用数据库操作
- `../ml_database_integration.py`: 机器学习数据集成
- `../DATABASE_README.md`: 数据库使用指南

## 📈 数据字段

爬取的招聘信息包含：
- 职位名称
- 公司名称
- 薪资范围
- 工作地点
- 工作经验要求
- 学历要求
- 职位描述
- 公司福利
- 发布时间

## ⚠️ 注意事项

1. **遵守robots.txt**: 尊重网站爬虫协议
2. **合理频率**: 避免对目标网站造成过大压力
3. **数据使用**: 仅用于学习和研究目的
4. **法律合规**: 确保爬取行为符合当地法律法规

## 🔧 依赖包

```bash
pip install aiohttp beautifulsoup4 selenium fake-useragent
pip install pandas numpy matplotlib seaborn scikit-learn
```

## 📖 详细文档

请查看 [JOB_SPIDER_README.md](JOB_SPIDER_README.md) 获取完整的使用说明和技术细节。
