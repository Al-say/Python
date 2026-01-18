"""
机器学习基础示例 - 分类算法
使用逻辑回归和决策树进行二分类任务
"""

import numpy as np
import pandas as pd
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns

def create_classification_dataset():
    """创建二分类数据集"""
    # 使用sklearn生成合成数据集
    X, y = make_classification(
        n_samples=1000,      # 样本数量
        n_features=4,        # 特征数量
        n_informative=3,     # 有信息的特征数量
        n_redundant=1,       # 冗余特征数量
        n_clusters_per_class=1,  # 每个类别的聚类数量
        random_state=42
    )

    # 转换为DataFrame便于理解
    feature_names = [f'特征{i+1}' for i in range(X.shape[1])]
    df = pd.DataFrame(X, columns=feature_names)
    df['目标变量'] = y

    return df, X, y

def train_logistic_regression(X_train, X_test, y_train, y_test):
    """训练逻辑回归模型"""
    print("=== 训练逻辑回归模型 ===")

    # 创建并训练模型
    model = LogisticRegression(random_state=42, max_iter=1000)
    model.fit(X_train, y_train)

    # 预测
    y_pred = model.predict(X_test)
    y_pred_proba = model.predict_proba(X_test)[:, 1]  # 正类概率

    # 评估模型
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)

    print(f"准确率: {accuracy:.4f}")
    print(f"精确率: {precision:.4f}")
    print(f"召回率: {recall:.4f}")
    print(f"F1分数: {f1:.4f}")
    print(f"模型系数: {model.coef_[0]}")
    print(f"模型截距: {model.intercept_[0]:.4f}")

    return model, y_pred, y_pred_proba

def train_decision_tree(X_train, X_test, y_train, y_test):
    """训练决策树模型"""
    print("\n=== 训练决策树模型 ===")

    # 创建并训练模型
    model = DecisionTreeClassifier(random_state=42, max_depth=3)
    model.fit(X_train, y_train)

    # 预测
    y_pred = model.predict(X_test)
    y_pred_proba = model.predict_proba(X_test)[:, 1]

    # 评估模型
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)

    print(f"准确率: {accuracy:.4f}")
    print(f"精确率: {precision:.4f}")
    print(f"召回率: {recall:.4f}")
    print(f"F1分数: {f1:.4f}")
    print(f"树的最大深度: {model.get_depth()}")
    print(f"叶子节点数量: {model.get_n_leaves()}")

    return model, y_pred, y_pred_proba

def plot_confusion_matrix(y_true, y_pred, title):
    """绘制混淆矩阵"""
    cm = confusion_matrix(y_true, y_pred)
    plt.figure(figsize=(6, 5))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
                xticklabels=['预测负类', '预测正类'],
                yticklabels=['实际负类', '实际正类'])
    plt.title(f'{title} - 混淆矩阵')
    plt.ylabel('实际标签')
    plt.xlabel('预测标签')
    plt.show()

def plot_feature_importance(model, feature_names, title):
    """绘制特征重要性"""
    if hasattr(model, 'feature_importances_'):
        importance = model.feature_importances_
        plt.figure(figsize=(8, 6))
        plt.bar(range(len(importance)), importance)
        plt.xticks(range(len(importance)), feature_names, rotation=45)
        plt.title(f'{title} - 特征重要性')
        plt.xlabel('特征')
        plt.ylabel('重要性')
        plt.tight_layout()
        plt.show()

def plot_decision_boundary(X, y, model, title):
    """绘制决策边界（仅适用于2D特征）"""
    if X.shape[1] != 2:
        return

    # 创建网格
    x_min, x_max = X[:, 0].min() - 1, X[:, 0].max() + 1
    y_min, y_max = X[:, 1].min() - 1, X[:, 1].max() + 1
    xx, yy = np.meshgrid(np.arange(x_min, x_max, 0.1),
                         np.arange(y_min, y_max, 0.1))

    # 预测网格点
    Z = model.predict(np.c_[xx.ravel(), yy.ravel()])
    Z = Z.reshape(xx.shape)

    # 绘制
    plt.figure(figsize=(8, 6))
    plt.contourf(xx, yy, Z, alpha=0.4, cmap='RdYlBu')
    plt.scatter(X[:, 0], X[:, 1], c=y, alpha=0.8, cmap='RdYlBu', edgecolors='black')
    plt.title(f'{title} - 决策边界')
    plt.xlabel('特征1')
    plt.ylabel('特征2')
    plt.show()

def main():
    print("=== 机器学习分类算法示例 ===\n")

    # 创建数据集
    df, X, y = create_classification_dataset()
    print("数据集信息:")
    print(f"样本数量: {len(df)}")
    print(f"特征数量: {X.shape[1]}")
    print(f"正类样本比例: {y.mean():.2%}")
    print(f"\n数据集预览:\n{df.head()}")

    # 划分训练集和测试集
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42, stratify=y
    )

    print(f"\n训练集大小: {len(X_train)}")
    print(f"测试集大小: {len(X_test)}")

    # 训练逻辑回归模型
    lr_model, lr_pred, lr_proba = train_logistic_regression(X_train, X_test, y_train, y_test)

    # 训练决策树模型
    dt_model, dt_pred, dt_proba = train_decision_tree(X_train, X_test, y_train, y_test)

    # 可视化结果
    feature_names = [f'特征{i+1}' for i in range(X.shape[1])]

    # 绘制混淆矩阵
    plot_confusion_matrix(y_test, lr_pred, "逻辑回归")
    plot_confusion_matrix(y_test, dt_pred, "决策树")

    # 绘制特征重要性（仅决策树）
    plot_feature_importance(dt_model, feature_names, "决策树")

    # 如果是2D数据，绘制决策边界
    if X.shape[1] == 2:
        plot_decision_boundary(X_test, y_test, lr_model, "逻辑回归")
        plot_decision_boundary(X_test, y_test, dt_model, "决策树")

    print("\n=== 模型比较 ===")
    models = {
        '逻辑回归': lr_pred,
        '决策树': dt_pred
    }

    for name, pred in models.items():
        acc = accuracy_score(y_test, pred)
        f1 = f1_score(y_test, pred)
        print(f"{name} - 准确率: {acc:.4f}, F1分数: {f1:.4f}")
    print("\n=== 分类算法学习完成 ===")
    print("主要概念:")
    print("- 逻辑回归: 适用于线性可分的二分类问题")
    print("- 决策树: 易解释，可处理非线性关系")
    print("- 评估指标: 准确率、精确率、召回率、F1分数")
    print("- 混淆矩阵: 显示分类结果的详细信息")

if __name__ == "__main__":
    main()
