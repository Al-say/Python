# Python机器学习学习项目

这是一个使用Python学习机器学习的项目，包含基础概念、算法实现和实际应用示例。

## 项目结构

```
machine_learning/
├── requirements.txt          # 项目依赖
├── basics/                   # 基础示例
│   ├── linear_regression.py  # 线性回归示例
│   ├── data_preprocessing.py # 数据预处理示例
│   └── classification.py     # 分类算法示例
├── datasets/                 # 数据集
└── models/                   # 训练好的模型
```

## 安装依赖

```bash
pip install -r requirements.txt
```

## 学习内容

### 1. 线性回归 (linear_regression.py)
- 学习目标：理解监督学习的基本概念
- 主要内容：
  - 数据生成和可视化
  - 线性回归模型训练
  - 模型评估（MSE、R²）
  - 结果可视化

### 2. 数据预处理 (data_preprocessing.py)
- 学习目标：掌握数据预处理的重要性
- 主要内容：
  - 处理缺失值
  - 检测和处理异常值
  - 特征编码（分类变量）
  - 数据标准化和归一化
  - 数据可视化

### 3. 分类算法 (classification.py)
- 学习目标：理解分类问题的解决方法
- 主要内容：
  - 逻辑回归算法
  - 决策树算法
  - 模型评估指标
  - 混淆矩阵分析
  - 特征重要性分析

## 运行示例

```bash
# 运行线性回归示例
python machine_learning/basics/linear_regression.py

# 运行数据预处理示例
python machine_learning/basics/data_preprocessing.py

# 运行分类算法示例
python machine_learning/basics/classification.py
```

## 学习建议

1. **循序渐进**：从线性回归开始，逐步学习更复杂的算法
2. **理解原理**：不要只关注代码，还要理解算法背后的数学原理
3. **实践为主**：多动手修改参数，观察结果变化
4. **理论结合**：学习理论知识的同时，通过代码验证理解

## 常用机器学习库

- **NumPy**: 数值计算基础
- **Pandas**: 数据处理和分析
- **Matplotlib**: 数据可视化
- **Seaborn**: 统计数据可视化
- **Scikit-learn**: 机器学习算法库

## 下一步学习计划

- [ ] 聚类算法 (K-means, 层次聚类)
- [ ] 支持向量机 (SVM)
- [ ] 神经网络基础
- [ ] 模型调参和交叉验证
- [ ] 特征选择和特征工程
- [ ] 模型集成方法
- [ ] 实际项目应用

## 参考资料

- [Scikit-learn官方文档](https://scikit-learn.org/)
- [机器学习实战](https://book.douban.com/subject/24703171/)
- [Python数据科学手册](https://book.douban.com/subject/27667378/)

---

**保持学习，享受编程的乐趣！** 🚀
