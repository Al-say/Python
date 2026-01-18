# 现代化招聘信息爬虫系统

## 📋 项目概述

这是一个使用最新技术的现代化招聘信息爬虫系统，集成了异步爬取、反爬虫策略、数据存储、可视化分析等功能。

## 🚀 核心特性

### 技术栈
- **异步爬取**: 使用 `aiohttp` 实现高并发
- **动态内容处理**: 集成 `Selenium` 处理 JavaScript 渲染
- **反爬虫策略**: 随机 User-Agent、请求延迟、代理池
- **数据存储**: SQLite 数据库存储招聘信息
- **数据分析**: Pandas + Matplotlib 进行数据分析和可视化
- **错误处理**: 完善的异常处理和重试机制

### 支持的数据源
- 🔍 **Boss直聘**: 国内领先的招聘平台
- 🔍 **拉勾网**: 互联网行业招聘平台
- 🔍 **Bilibili招聘**: B站内部招聘频道

## 📁 文件结构

```
web_scraping/
├── job_spider.py          # 完整版现代化爬虫
├── job_spider_demo.py     # 演示版爬虫（推荐学习使用）
├── job_demo.db           # 演示数据数据库
├── job_analysis_demo.png # 数据可视化图表
├── job_report_demo.md    # 分析报告
└── JOB_SPIDER_README.md  # 本说明文档
```

## 🔗 相关文件

- `../database_connection.py` - 通用数据库连接示例
- `../ml_database_integration.py` - 机器学习数据库集成
- `../DATABASE_README.md` - 数据库使用指南

## 🛠️ 环境准备

### 1. 安装依赖

```bash
# 安装基础依赖
pip install aiohttp beautifulsoup4 selenium fake-useragent requests

# 安装机器学习和数据分析依赖
pip install pandas numpy matplotlib seaborn scikit-learn

# 安装数据库依赖
pip install sqlalchemy

# 可选：安装 Chrome WebDriver
pip install webdriver-manager
```

### 2. ChromeDriver 设置

对于需要 Selenium 的网站，系统会自动下载 ChromeDriver。

## 🎯 快速开始

### 演示版本（推荐新手）

```python
from job_spider_demo import SimpleJobSpider

# 初始化爬虫
spider = SimpleJobSpider()

# 爬取演示数据
boss_jobs = spider.crawl_zhipin_demo("Python", pages=2)
lagou_jobs = spider.crawl_lagou_demo("Python", pages=2)

# 保存到数据库
spider.save_jobs_to_db(boss_jobs + lagou_jobs)

# 分析和可视化
spider.analyze_and_visualize()

# 关闭连接
spider.close()
```

### 完整版本（生产环境）

```python
import asyncio
from job_spider import JobSpider

async def main():
    # 初始化爬虫
    spider = JobSpider()

    # 运行完整爬取流程
    await spider.run_crawler("Python工程师", max_pages=3)

    # 关闭资源
    await spider.close()

# 运行
asyncio.run(main())
```

## 📊 数据结构

### 招聘信息表 (jobs)
```sql
CREATE TABLE jobs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    job_id TEXT UNIQUE,           -- 职位唯一标识
    title TEXT NOT NULL,          -- 职位标题
    company TEXT NOT NULL,        -- 公司名称
    salary TEXT,                  -- 薪资范围
    location TEXT,                -- 工作地点
    experience TEXT,              -- 经验要求
    education TEXT,               -- 学历要求
    description TEXT,             -- 职位描述
    tags TEXT,                    -- 标签(JSON格式)
    source TEXT,                  -- 数据来源
    url TEXT,                     -- 原始链接
    publish_time TEXT,            -- 发布时间
    crawl_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 公司信息表 (companies)
```sql
CREATE TABLE companies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE,
    industry TEXT,
    size TEXT,
    description TEXT,
    website TEXT,
    logo_url TEXT
);
```

## 🔧 高级配置

### 自定义数据源

```python
# 在 JobSpider.sources 中添加新的数据源
self.sources['new_source'] = {
    'name': '新招聘网站',
    'base_url': 'https://example.com',
    'search_url': 'https://example.com/search?keyword={keyword}&page={page}',
    'parser': self.parse_new_source
}
```

### 反爬虫策略配置

```python
# 调整请求参数
self.request_delay = (2, 5)  # 2-5秒随机延迟
self.max_retries = 5         # 最大重试次数
self.timeout = 60            # 请求超时时间
```

### 代理池设置

```python
# 添加代理支持
proxies = {
    'http': 'http://proxy.example.com:8080',
    'https': 'https://proxy.example.com:8080'
}

async with self.session.get(url, proxy=proxies['https']) as response:
    # 请求代码
```

## 📈 数据分析功能

### 自动生成分析报告
- 📊 数据源分布统计
- 💰 薪资范围分析
- 🏢 热门公司排名
- 📍 工作地点分布
- 🏷️ 职位标签分析

### 可视化图表
- 饼图：数据源分布
- 直方图：薪资分布
- 条形图：地点和公司统计
- 热力图：相关性分析

## ⚠️ 法律与道德提醒

### 遵守法律法规
- ✅ 仅用于学习和研究目的
- ✅ 遵守网站的服务条款
- ✅ 尊重 robots.txt 文件
- ❌ 禁止用于商业用途
- ❌ 禁止过度频繁请求
- ❌ 禁止窃取用户数据

### 最佳实践
1. **限制请求频率**: 使用合理的延迟
2. **识别爬虫**: 设置合适的 User-Agent
3. **数据清理**: 及时清理测试数据
4. **备份数据**: 重要数据定期备份

## 🔍 故障排除

### 常见问题

**Q: 网站请求被拒绝？**
A: 尝试调整 User-Agent 或增加延迟时间

**Q: Selenium 无法启动？**
A: 确保 Chrome 浏览器已安装，或使用 headless 模式

**Q: 数据解析失败？**
A: 检查网站 HTML 结构是否改变，更新选择器

**Q: 数据库连接错误？**
A: 检查 SQLite 文件权限，或使用其他数据库

### 调试模式

```python
import logging
logging.basicConfig(level=logging.DEBUG)

# 启用详细日志
spider = JobSpider()
```

## 🚀 扩展功能

### 计划中的功能
- [ ] 支持更多招聘网站
- [ ] 实时数据更新
- [ ] 职位推荐算法
- [ ] REST API 接口
- [ ] 分布式爬取
- [ ] 数据导出功能

### 自定义扩展

```python
# 继承 JobSpider 类
class CustomJobSpider(JobSpider):
    def custom_analysis(self):
        # 添加自定义分析逻辑
        pass
```

## 📞 技术支持

如有问题或建议，请：

1. 查看项目文档
2. 检查常见问题解答
3. 提交 Issue 描述问题
4. 贡献代码改进功能

## 📄 开源协议

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

---

**最后更新**: 2026年1月18日
**版本**: v1.0.0
