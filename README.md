# Python学习项目

本项目是一个综合性的Python学习环境，包含机器学习、数据库操作、网络爬虫等多个模块。

## 📁 项目结构

### 🔬 机器学习模块 (`machine_learning/`)
- **basics/**: 基础算法实现
  - `classification.py` - 分类算法
  - `data_preprocessing.py` - 数据预处理
  - `linear_regression.py` - 线性回归
- **datasets/**: 数据集存储
- **models/**: 训练好的模型
- **requirements.txt**: 依赖包列表

### 🕷️ 网络爬虫模块 (`web_scraping/`)
- **job_spider.py**: 招聘信息爬虫主程序
- **job_spider_demo.py**: 爬虫功能演示
- **job_demo.db**: 爬取的数据存储
- **job_analysis_demo.png**: 数据分析可视化
- **job_report_demo.md**: 分析报告
- **JOB_SPIDER_README.md**: 爬虫使用说明

### 🗄️ 数据库模块
- **database_connection.py**: 通用数据库连接示例
- **ml_database_integration.py**: 机器学习数据库集成
- **DATABASE_README.md**: 数据库使用指南
- **python_learning.db**: 示例数据库
- **ml_experiments.db**: 机器学习实验数据库

### 🔐 密码检查器 (`password_checker/`)
- **strength.py**: 密码强度检查逻辑
- **ui.py**: 用户界面
- **validator.py**: 密码验证器
- **__init__.py**: 包初始化

### 📊 实验报告 (`reports/`)
- 包含各实验的PDF和Markdown格式报告

### 🎯 实验代码 (`experiments/`)
- **exp3/**: 实验三相关代码
- **exp4/**: 实验四相关代码
- **exp5/**: 实验五相关代码

### 📚 资源文件 (`resources/`)
- 实验指导书和相关资料

## 🚀 快速开始

### 环境设置
```bash
# 使用批处理脚本设置Python环境
set_python313.bat

# 或使用PowerShell脚本
.\set_python313.ps1
```

### 安装依赖
```bash
pip install -r machine_learning/requirements.txt
```

## 🛠️ 主要功能

### 1. 机器学习实验
```bash
cd machine_learning
python basics/linear_regression.py
```

### 2. 数据库操作
```bash
# 通用数据库连接
python database_connection.py

# 机器学习数据库集成
python ml_database_integration.py
```

### 3. 网络爬虫
```bash
cd web_scraping
python job_spider_demo.py
```

### 4. 密码检查器
```bash
cd password_checker
python ui.py
```

## 📋 依赖包

主要依赖包已列在 `machine_learning/requirements.txt` 中：
- numpy, pandas, matplotlib, seaborn
- scikit-learn, jupyter
- 数据库连接库：mysql-connector-python, psycopg2-binary, pymongo, SQLAlchemy

## 🔧 开发环境

- **Python版本**: 3.13.11
- **操作系统**: Windows
- **IDE**: VS Code (推荐)
- **版本控制**: Git

## 📖 使用说明

每个模块都有详细的使用说明：

- [数据库使用指南](DATABASE_README.md)
- [爬虫使用说明](web_scraping/JOB_SPIDER_README.md)
- [Python环境设置](PYTHON_SETUP_README.md)

## 🤝 贡献

欢迎提交Issue和Pull Request来改进项目！

## 📄 许可证

本项目采用MIT许可证 - 查看[LICENSE](LICENSE)文件了解详情。
