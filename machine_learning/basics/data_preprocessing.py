"""
机器学习基础示例 - 数据预处理
演示数据清洗、特征工程和标准化等预处理技术
"""

import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler, MinMaxScaler, LabelEncoder
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import seaborn as sns

def create_sample_dataset():
    """创建包含缺失值和异常值的示例数据集"""
    np.random.seed(42)

    # 创建基础数据
    data = {
        'age': np.random.normal(35, 10, 100),
        'income': np.random.normal(50000, 15000, 100),
        'education': np.random.choice(['高中', '本科', '硕士', '博士'], 100),
        'experience': np.random.normal(10, 5, 100),
        'city': np.random.choice(['北京', '上海', '广州', '深圳'], 100)
    }

    df = pd.DataFrame(data)

    # 添加缺失值
    mask = np.random.random(100) < 0.1  # 10%的缺失率
    df.loc[mask, 'income'] = np.nan

    # 添加异常值
    outlier_indices = np.random.choice(100, 5, replace=False)
    df.loc[outlier_indices, 'income'] = df.loc[outlier_indices, 'income'] * 10

    return df

def handle_missing_values(df):
    """处理缺失值"""
    print("=== 处理缺失值 ===")
    print(f"原始数据缺失值统计:\n{df.isnull().sum()}")

    # 使用中位数填充数值型缺失值
    imputer = SimpleImputer(strategy='median')
    df['income_filled'] = imputer.fit_transform(df[['income']])

    print(f"\n填充后缺失值统计:\n{df[['income', 'income_filled']].isnull().sum()}")
    return df

def handle_outliers(df, column):
    """处理异常值"""
    print(f"\n=== 处理 {column} 列的异常值 ===")

    # 计算IQR
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1

    # 定义异常值边界
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    print(f"Q1: {Q1:.2f}, Q3: {Q3:.2f}, IQR: {IQR:.2f}")
    print(f"异常值边界: [{lower_bound:.2f}, {upper_bound:.2f}]")

    # 识别异常值
    outliers = (df[column] < lower_bound) | (df[column] > upper_bound)
    print(f"异常值数量: {outliers.sum()}")

    # 用边界值替换异常值
    df[f'{column}_cleaned'] = df[column].clip(lower_bound, upper_bound)

    return df

def encode_categorical_features(df):
    """编码分类特征"""
    print("\n=== 编码分类特征 ===")

    # 标签编码
    le = LabelEncoder()
    df['education_encoded'] = le.fit_transform(df['education'])
    df['city_encoded'] = le.fit_transform(df['city'])

    print("教育水平编码映射:")
    for i, label in enumerate(le.classes_):
        print(f"  {label} -> {i}")

    print("\n城市编码映射:")
    le_city = LabelEncoder()
    df['city_encoded'] = le_city.fit_transform(df['city'])
    for i, label in enumerate(le_city.classes_):
        print(f"  {label} -> {i}")

    return df

def scale_numerical_features(df):
    """标准化数值特征"""
    print("\n=== 标准化数值特征 ===")

    numerical_cols = ['age', 'income_filled', 'experience']

    # 标准化 (Z-score)
    scaler = StandardScaler()
    df_scaled = df.copy()
    df_scaled[numerical_cols] = scaler.fit_transform(df[numerical_cols])

    print("标准化后的统计信息:")
    print(df_scaled[numerical_cols].describe().round(3))

    # 归一化 (Min-Max)
    minmax_scaler = MinMaxScaler()
    df_normalized = df.copy()
    df_normalized[numerical_cols] = minmax_scaler.fit_transform(df[numerical_cols])

    print("\n归一化后的统计信息:")
    print(df_normalized[numerical_cols].describe().round(3))

    return df_scaled, df_normalized

def visualize_data(df):
    """可视化数据分布"""
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))

    # 年龄分布
    axes[0, 0].hist(df['age'], bins=20, alpha=0.7, color='blue')
    axes[0, 0].set_title('年龄分布')
    axes[0, 0].set_xlabel('年龄')
    axes[0, 0].set_ylabel('频次')

    # 收入分布（包含异常值）
    axes[0, 1].hist(df['income'], bins=20, alpha=0.7, color='red')
    axes[0, 1].set_title('收入分布（原始）')
    axes[0, 1].set_xlabel('收入')
    axes[0, 1].set_ylabel('频次')

    # 收入分布（处理后）
    if 'income_cleaned' in df.columns:
        axes[1, 0].hist(df['income_cleaned'], bins=20, alpha=0.7, color='green')
        axes[1, 0].set_title('收入分布（处理异常值后）')
        axes[1, 0].set_xlabel('收入')
        axes[1, 0].set_ylabel('频次')

    # 教育水平分布
    education_counts = df['education'].value_counts()
    axes[1, 1].bar(education_counts.index, education_counts.values, alpha=0.7, color='purple')
    axes[1, 1].set_title('教育水平分布')
    axes[1, 1].set_xlabel('教育水平')
    axes[1, 1].set_ylabel('数量')
    axes[1, 1].tick_params(axis='x', rotation=45)

    plt.tight_layout()
    plt.show()

def main():
    print("=== 机器学习数据预处理示例 ===\n")

    # 创建数据集
    df = create_sample_dataset()
    print("原始数据集信息:")
    print(f"数据形状: {df.shape}")
    print(f"数据类型:\n{df.dtypes}")
    print(f"\n前5行数据:\n{df.head()}")

    # 处理缺失值
    df = handle_missing_values(df)

    # 处理异常值
    df = handle_outliers(df, 'income_filled')

    # 编码分类特征
    df = encode_categorical_features(df)

    # 标准化数值特征
    df_scaled, df_normalized = scale_numerical_features(df)

    # 可视化
    visualize_data(df)

    print("\n=== 数据预处理完成 ===")
    print(f"最终数据集形状: {df.shape}")
    print(f"特征数量: {len(df.columns)}")
    print(f"数值特征: {['age', 'income_filled', 'experience', 'education_encoded', 'city_encoded']}")
    print(f"分类特征: {['education', 'city']}")

if __name__ == "__main__":
    main()
