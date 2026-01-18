# 机器学习数据库集成示例
# 将机器学习实验结果存储到数据库中

import sqlite3
import json
import pandas as pd
import numpy as np
from datetime import datetime
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

class MLDatabaseManager:
    """机器学习数据库管理器"""

    def __init__(self, db_path='ml_experiments.db'):
        """初始化数据库连接"""
        self.db_path = db_path
        self.connection = sqlite3.connect(db_path)
        self.create_tables()
        print(f"✅ 连接到机器学习数据库: {db_path}")

    def create_tables(self):
        """创建机器学习实验相关的表"""
        cursor = self.connection.cursor()

        # 实验记录表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS experiments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                experiment_name TEXT NOT NULL,
                model_type TEXT NOT NULL,
                dataset_name TEXT,
                parameters TEXT,  -- JSON格式存储模型参数
                metrics TEXT,     -- JSON格式存储评估指标
                feature_importance TEXT,  -- JSON格式存储特征重要性
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                status TEXT DEFAULT 'running'  -- running, completed, failed
            )
        ''')

        # 数据集信息表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS datasets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                description TEXT,
                rows INTEGER,
                columns INTEGER,
                data_types TEXT,  -- JSON格式存储各列数据类型
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # 模型性能对比表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS model_comparison (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                experiment_id INTEGER,
                model_name TEXT NOT NULL,
                accuracy REAL,
                precision REAL,
                recall REAL,
                f1_score REAL,
                auc REAL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (experiment_id) REFERENCES experiments (id)
            )
        ''')

        self.connection.commit()
        print("✅ 机器学习数据库表创建完成")

    def save_dataset_info(self, name, description, dataframe):
        """保存数据集信息"""
        cursor = self.connection.cursor()

        # 获取数据类型信息
        data_types = {}
        for column in dataframe.columns:
            data_types[column] = str(dataframe[column].dtype)

        cursor.execute('''
            INSERT OR REPLACE INTO datasets (name, description, rows, columns, data_types)
            VALUES (?, ?, ?, ?, ?)
        ''', (name, description, len(dataframe), len(dataframe.columns), json.dumps(data_types)))

        self.connection.commit()
        print(f"✅ 数据集 '{name}' 信息已保存")

    def save_experiment(self, experiment_name, model_type, dataset_name, parameters,
                       metrics, feature_importance=None):
        """保存实验结果"""
        cursor = self.connection.cursor()

        cursor.execute('''
            INSERT INTO experiments (experiment_name, model_type, dataset_name,
                                   parameters, metrics, feature_importance, status)
            VALUES (?, ?, ?, ?, ?, ?, 'completed')
        ''', (experiment_name, model_type, dataset_name,
              json.dumps(parameters), json.dumps(metrics),
              json.dumps(feature_importance) if feature_importance else None))

        experiment_id = cursor.lastrowid
        self.connection.commit()
        print(f"✅ 实验 '{experiment_name}' 结果已保存 (ID: {experiment_id})")
        return experiment_id

    def get_experiments(self, limit=10):
        """获取实验记录"""
        cursor = self.connection.cursor()
        cursor.execute('''
            SELECT id, experiment_name, model_type, dataset_name,
                   metrics, created_at, status
            FROM experiments
            ORDER BY created_at DESC
            LIMIT ?
        ''', (limit,))

        experiments = cursor.fetchall()
        result = []
        for exp in experiments:
            result.append({
                'id': exp[0],
                'experiment_name': exp[1],
                'model_type': exp[2],
                'dataset_name': exp[3],
                'metrics': json.loads(exp[4]) if exp[4] else {},
                'created_at': exp[5],
                'status': exp[6]
            })

        return result

    def run_linear_regression_experiment(self, experiment_name="线性回归实验"):
        """运行线性回归实验并保存结果"""
        print(f"\n🧪 运行实验: {experiment_name}")

        # 生成示例数据集
        np.random.seed(42)
        X = np.random.randn(100, 3)
        y = 2*X[:, 0] + 3*X[:, 1] - X[:, 2] + np.random.randn(100) * 0.1

        # 转换为DataFrame
        df = pd.DataFrame(X, columns=['feature1', 'feature2', 'feature3'])
        df['target'] = y

        # 保存数据集信息
        self.save_dataset_info("linear_regression_sample", "线性回归示例数据集", df)

        # 分割数据
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # 训练模型
        model = LinearRegression()
        model.fit(X_train, y_train)

        # 预测
        y_pred = model.predict(X_test)

        # 计算指标
        mse = mean_squared_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)

        # 准备保存的数据
        parameters = {
            'model': 'LinearRegression',
            'test_size': 0.2,
            'random_state': 42
        }

        metrics = {
            'mean_squared_error': mse,
            'r2_score': r2,
            'coefficients': model.coef_.tolist(),
            'intercept': model.intercept_
        }

        feature_importance = {
            'feature1': abs(model.coef_[0]),
            'feature2': abs(model.coef_[1]),
            'feature3': abs(model.coef_[2])
        }

        # 保存实验结果
        experiment_id = self.save_experiment(
            experiment_name=experiment_name,
            model_type='LinearRegression',
            dataset_name='linear_regression_sample',
            parameters=parameters,
            metrics=metrics,
            feature_importance=feature_importance
        )

        print(f"📈 模型性能 - MSE: {mse:.4f}, R²: {r2:.4f}")
        return experiment_id

    def compare_experiments(self):
        """比较实验结果"""
        experiments = self.get_experiments()

        if not experiments:
            print("❌ 没有找到实验记录")
            return

        print("\n📊 实验结果对比:")
        print("-" * 80)
        print(f"{'实验名称':<20} {'模型类型':<15} {'MSE':<12} {'R²':<12} {'状态':<10}")
        print("-" * 80)

        for exp in experiments:
            metrics = exp['metrics']
            mse = metrics.get('mean_squared_error', 'N/A')
            r2 = metrics.get('r2_score', 'N/A')

            mse_str = f"{mse:.4f}" if isinstance(mse, (int, float)) else str(mse)
            r2_str = f"{r2:.4f}" if isinstance(r2, (int, float)) else str(r2)

            print(f"{exp['experiment_name']:<20} {exp['model_type']:<15} {mse_str:<12} {r2_str:<12} {exp['status']:<10}")

    def close(self):
        """关闭数据库连接"""
        if self.connection:
            self.connection.close()
            print("🔌 数据库连接已关闭")


def main():
    """主函数 - 演示机器学习数据库集成"""
    print("🚀 机器学习数据库集成演示")
    print("=" * 60)

    # 1. 初始化数据库
    print("\n1️⃣ 初始化数据库...")
    db = MLDatabaseManager('ml_experiments.db')

    # 2. 运行线性回归实验
    print("\n2️⃣ 运行线性回归实验...")
    experiment_id = db.run_linear_regression_experiment("线性回归示例实验")

    # 3. 查看实验结果
    print("\n3️⃣ 查看实验结果...")
    db.compare_experiments()

    # 4. 关闭连接
    print("\n4️⃣ 关闭数据库连接...")
    db.close()

    print("\n" + "=" * 60)
    print("✅ 机器学习数据库集成演示完成!")
    print("\n💡 提示:")
    print("- 数据库文件: ml_experiments.db")
    print("- 可以扩展支持更多机器学习算法")
    print("- 支持实验结果的历史记录和对比")


if __name__ == "__main__":
    main()
