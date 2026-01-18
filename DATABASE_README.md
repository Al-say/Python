# Python数据库连接指南

本项目提供了完整的Python数据库连接和集成功能，支持多种数据库类型。

## 📁 文件说明

### 数据库连接文件
- `database_connection.py` - 通用数据库连接示例
- `ml_database_integration.py` - 机器学习数据库集成示例
- `python_learning.db` - SQLite示例数据库
- `ml_experiments.db` - 机器学习实验数据库

## 🗄️ 支持的数据库类型

### 1. SQLite (推荐用于学习)
- **优点**: 无需安装服务器，文件数据库，Python内置支持
- **使用场景**: 学习、开发、小型项目
- **文件**: `python_learning.db`

### 2. MySQL
- **安装**: `pip install mysql-connector-python`
- **使用**: 企业级应用，生产环境

### 3. PostgreSQL
- **安装**: `pip install psycopg2-binary`
- **使用**: 复杂查询，地理数据，企业应用

### 4. MongoDB
- **安装**: `pip install pymongo`
- **使用**: NoSQL数据库，文档型数据

## 🚀 快速开始

### 基本数据库连接
```bash
python database_connection.py
```

### 机器学习数据库集成
```bash
python ml_database_integration.py
```

## 📊 数据库结构

### 用户表 (users)
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL,
    password_hash TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT 1
);
```

### 实验表 (experiments)
```sql
CREATE TABLE experiments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    experiment_name TEXT NOT NULL,
    description TEXT,
    data TEXT,  -- JSON格式存储实验数据
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users (id)
);
```

### 机器学习实验表 (ml_experiments)
```sql
CREATE TABLE experiments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    experiment_name TEXT NOT NULL,
    model_type TEXT NOT NULL,
    dataset_name TEXT,
    parameters TEXT,     -- JSON格式存储模型参数
    metrics TEXT,        -- JSON格式存储评估指标
    feature_importance TEXT,  -- JSON格式存储特征重要性
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status TEXT DEFAULT 'running'
);
```

## 🔧 安装依赖

```bash
# 安装数据库连接库
pip install mysql-connector-python psycopg2-binary pymongo SQLAlchemy

# 或使用requirements.txt
pip install -r machine_learning/requirements.txt
```

## 💡 使用示例

### 连接SQLite数据库
```python
from database_connection import DatabaseManager

# 连接数据库
db = DatabaseManager('sqlite', database='my_database.db')

# 创建表
db.create_tables()

# 插入数据
db.insert_sample_data()

# 查询数据
db.query_data()

# 关闭连接
db.close()
```

### 机器学习实验记录
```python
from ml_database_integration import MLDatabaseManager

# 初始化
db = MLDatabaseManager('ml_experiments.db')

# 运行实验并保存结果
experiment_id = db.run_linear_regression_experiment("我的实验")

# 查看实验对比
db.compare_experiments()

# 关闭连接
db.close()
```

## 🔒 安全注意事项

1. **不要将数据库文件提交到Git**: 已添加到`.gitignore`
2. **生产环境使用环境变量**: 不要硬编码数据库密码
3. **使用参数化查询**: 防止SQL注入攻击
4. **定期备份**: 重要数据要定期备份

## 📈 扩展功能

- [ ] 添加数据可视化功能
- [ ] 支持更多机器学习算法
- [ ] 添加用户认证系统
- [ ] 实现数据导入导出功能
- [ ] 添加REST API接口

## 🤝 贡献

欢迎提交Issue和Pull Request来改进数据库功能！

## 📄 许可证

本项目采用MIT许可证 - 查看[LICENSE](LICENSE)文件了解详情。
