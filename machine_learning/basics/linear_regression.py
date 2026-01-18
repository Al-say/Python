"""
机器学习基础示例 - 线性回归
使用scikit-learn实现简单的线性回归
"""

import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score

def create_sample_data():
    """创建示例数据集"""
    # 生成一些随机数据
    np.random.seed(42)
    X = np.random.rand(100, 1) * 10
    y = 2 * X + 1 + np.random.randn(100, 1) * 2  # y = 2x + 1 + 噪声

    return X, y

def train_linear_regression(X, y):
    """训练线性回归模型"""
    # 划分训练集和测试集
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # 创建并训练模型
    model = LinearRegression()
    model.fit(X_train, y_train)

    # 预测
    y_pred = model.predict(X_test)

    # 评估模型
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    print("线性回归模型结果：")
    print(f"斜率 (coefficient): {model.coef_[0][0]:.2f}")
    print(f"截距 (intercept): {model.intercept_[0]:.2f}")
    print(f"均方误差 (MSE): {mse:.2f}")
    print(f"R² 得分: {r2:.2f}")

    return model, X_test, y_test, y_pred

def plot_results(X, y, model, X_test, y_test, y_pred):
    """可视化结果"""
    plt.figure(figsize=(10, 6))

    # 绘制原始数据点
    plt.scatter(X, y, color='blue', alpha=0.5, label='原始数据')

    # 绘制回归线
    X_range = np.linspace(X.min(), X.max(), 100).reshape(-1, 1)
    y_range = model.predict(X_range)
    plt.plot(X_range, y_range, color='red', linewidth=2, label='回归线')

    # 绘制测试集预测结果
    plt.scatter(X_test, y_pred, color='green', marker='x', s=100, label='预测值')

    plt.xlabel('X')
    plt.ylabel('y')
    plt.title('线性回归示例')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.show()

def main():
    print("=== 机器学习基础：线性回归示例 ===\n")

    # 创建数据
    X, y = create_sample_data()
    print(f"数据集大小: {len(X)} 个样本")
    print(f"X 范围: [{X.min():.2f}, {X.max():.2f}]")
    print(f"y 范围: [{y.min():.2f}, {y.max():.2f}]\n")

    # 训练模型
    model, X_test, y_test, y_pred = train_linear_regression(X, y)

    # 可视化结果
    plot_results(X, y, model, X_test, y_test, y_pred)

if __name__ == "__main__":
    main()
