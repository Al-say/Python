# Python数据库连接示例
# 支持SQLite、MySQL、PostgreSQL等多种数据库

import sqlite3
import os
from datetime import datetime

class DatabaseManager:
    """数据库管理器类"""

    def __init__(self, db_type='sqlite', **kwargs):
        """
        初始化数据库连接

        Args:
            db_type: 数据库类型 ('sqlite', 'mysql', 'postgresql')
            **kwargs: 数据库连接参数
        """
        self.db_type = db_type
        self.connection = None

        if db_type == 'sqlite':
            # SQLite数据库
            db_path = kwargs.get('database', 'example.db')
            self.connection = sqlite3.connect(db_path)
            print(f"✅ 连接到SQLite数据库: {db_path}")

        elif db_type == 'mysql':
            # MySQL数据库 (需要安装: pip install mysql-connector-python)
            try:
                import mysql.connector
                self.connection = mysql.connector.connect(
                    host=kwargs.get('host', 'localhost'),
                    user=kwargs.get('user', 'root'),
                    password=kwargs.get('password', ''),
                    database=kwargs.get('database', 'test'),
                    port=kwargs.get('port', 3306)
                )
                print("✅ 连接到MySQL数据库")
            except ImportError:
                print("❌ 请先安装MySQL连接器: pip install mysql-connector-python")

        elif db_type == 'postgresql':
            # PostgreSQL数据库 (需要安装: pip install psycopg2)
            try:
                import psycopg2
                self.connection = psycopg2.connect(
                    host=kwargs.get('host', 'localhost'),
                    user=kwargs.get('user', 'postgres'),
                    password=kwargs.get('password', ''),
                    database=kwargs.get('database', 'test'),
                    port=kwargs.get('port', 5432)
                )
                print("✅ 连接到PostgreSQL数据库")
            except ImportError:
                print("❌ 请先安装PostgreSQL连接器: pip install psycopg2-binary")

        else:
            raise ValueError(f"不支持的数据库类型: {db_type}")

    def create_tables(self):
        """创建示例表"""
        if not self.connection:
            return

        cursor = self.connection.cursor()

        if self.db_type == 'sqlite':
            # 创建用户表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL UNIQUE,
                    email TEXT NOT NULL,
                    password_hash TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    is_active BOOLEAN DEFAULT 1
                )
            ''')

            # 创建实验数据表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS experiments (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    experiment_name TEXT NOT NULL,
                    description TEXT,
                    data TEXT,  -- JSON格式存储实验数据
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )
            ''')

        print("✅ 数据表创建完成")

    def insert_sample_data(self):
        """插入示例数据"""
        if not self.connection:
            return

        cursor = self.connection.cursor()

        try:
            # 插入用户数据
            cursor.execute('''
                INSERT OR IGNORE INTO users (username, email, password_hash)
                VALUES (?, ?, ?)
            ''', ('admin', 'admin@example.com', 'hashed_password_123'))

            cursor.execute('''
                INSERT OR IGNORE INTO users (username, email, password_hash)
                VALUES (?, ?, ?)
            ''', ('user1', 'user1@example.com', 'hashed_password_456'))

            # 插入实验数据
            cursor.execute('''
                INSERT INTO experiments (user_id, experiment_name, description, data)
                VALUES (?, ?, ?, ?)
            ''', (1, '机器学习实验1', '线性回归实验', '{"accuracy": 0.85, "model": "linear_regression"}'))

            cursor.execute('''
                INSERT INTO experiments (user_id, experiment_name, description, data)
                VALUES (?, ?, ?, ?)
            ''', (1, '机器学习实验2', '分类实验', '{"accuracy": 0.92, "model": "random_forest"}'))

            self.connection.commit()
            print("✅ 示例数据插入完成")

        except Exception as e:
            print(f"❌ 插入数据时出错: {e}")
            self.connection.rollback()

    def query_data(self):
        """查询数据示例"""
        if not self.connection:
            return

        cursor = self.connection.cursor()

        try:
            # 查询所有用户
            cursor.execute("SELECT id, username, email, created_at FROM users")
            users = cursor.fetchall()
            print("\n📋 用户列表:")
            for user in users:
                print(f"ID: {user[0]}, 用户名: {user[1]}, 邮箱: {user[2]}, 创建时间: {user[3]}")

            # 查询实验数据
            cursor.execute("""
                SELECT e.experiment_name, e.description, u.username, e.created_at
                FROM experiments e
                JOIN users u ON e.user_id = u.id
                ORDER BY e.created_at DESC
            """)
            experiments = cursor.fetchall()
            print("\n🧪 实验列表:")
            for exp in experiments:
                print(f"实验名: {exp[0]}, 描述: {exp[1]}, 用户: {exp[2]}, 创建时间: {exp[3]}")

        except Exception as e:
            print(f"❌ 查询数据时出错: {e}")

    def close(self):
        """关闭数据库连接"""
        if self.connection:
            self.connection.close()
            print("🔌 数据库连接已关闭")


def main():
    """主函数 - 演示数据库连接和操作"""
    print("🚀 Python数据库连接演示")
    print("=" * 50)

    # 1. 连接SQLite数据库 (推荐用于学习)
    print("\n1️⃣ 连接SQLite数据库...")
    db = DatabaseManager('sqlite', database='python_learning.db')

    # 2. 创建表
    print("\n2️⃣ 创建数据表...")
    db.create_tables()

    # 3. 插入示例数据
    print("\n3️⃣ 插入示例数据...")
    db.insert_sample_data()

    # 4. 查询数据
    print("\n4️⃣ 查询数据...")
    db.query_data()

    # 5. 关闭连接
    print("\n5️⃣ 关闭数据库连接...")
    db.close()

    print("\n" + "=" * 50)
    print("✅ 数据库操作演示完成!")
    print("\n💡 提示:")
    print("- SQLite数据库文件已创建: python_learning.db")
    print("- 如需使用MySQL/PostgreSQL，请先安装相应驱动")
    print("- 可以修改DatabaseManager类来扩展更多功能")


if __name__ == "__main__":
    main()
