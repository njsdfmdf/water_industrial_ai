import pandas as pd
import numpy as np
import torch
import io

# ==========================================
# Step 0: 模拟真实数据 (实际工作中这一步是读取文件)
# ==========================================
csv_content = """Time,PH,Turbidity,Temp,Quality
2026-01-26 09:00,7.2,15.5,22.5,Good
2026-01-26 10:00,6.5,55.2,23.1,Bad
2026-01-26 11:00,7.8,12.3,22.0,Good
2026-01-26 12:00,5.9,60.5,24.5,Bad
2026-01-26 13:00,7.1,18.2,22.8,Good"""

# 使用 StringIO 模拟读取硬盘上的 csv 文件
# 实际代码: df = pd.read_csv('water_quality.csv')
df = pd.read_csv(io.StringIO(csv_content))

print("=== 1. 原始 Pandas 数据表 (人类可读) ===")
print(df)


# ==========================================
# Step 1: 数据清洗 (Pandas)
# ==========================================
print("\n=== 2. 开始清洗数据 ===")

# 1.1 剔除无关列
# 时间戳虽然重要，但如果不是做时序预测(RNN)，普通模型通常处理不了字符串时间
# 所以我们把 'Time' 这一列扔掉
df_clean = df.drop(['Time'], axis=1)

# 1.2 标签数值化 (Encoding)
# 机器看不懂 "Good"/"Bad"，必须转成 0/1
# 工业界标准：通常把关注的负面/异常情况设为 1 (Positive Class)，正常设为 0
label_mapping = {'Good': 0, 'Bad': 1}
df_clean['Quality'] = df_clean['Quality'].map(label_mapping)

print("清洗后的数据表:")
print(df_clean)


# ==========================================
# Step 2: 特征与标签分离 (Pandas -> NumPy)
# ==========================================
print("\n=== 3. 分离特征(X)与标签(y) ===")

# 提取特征：所有行，除了最后一列
# .values 将 Pandas DataFrame 转换为 NumPy 数组
X_numpy = df_clean.iloc[:, :-1].values 

# 提取标签：所有行，只取最后一列
y_numpy = df_clean.iloc[:, -1].values

print(f"X (NumPy) shape: {X_numpy.shape}") # (5, 3) -> 5条数据, 3个特征(PH, 浊度, 温度)
print(f"y (NumPy) shape: {y_numpy.shape}") # (5,)   -> 5个答案


# ==========================================
# Step 3: 数据标准化 (Normalization) - ⚠️工业界核心步骤
# ==========================================
# 原始数据里，浊度可能是 50.0，PH值是 7.0。
# 50 比 7 大太多，会让模型以为浊度更重要。
# 我们必须把它们缩放到同一个起跑线 (通常是 0附近)。
print("\n=== 4. 数据标准化 (Normalization) ===")

# 计算每一列的均值和标准差
mean = X_numpy.mean(axis=0)
std = X_numpy.std(axis=0)

# 公式: (X - mean) / std
X_scaled = (X_numpy - mean) / std

print("标准化后的 X (前2行):\n", X_scaled[:2])


# ==========================================
# Step 4: 转换为 Tensor (PyTorch)
# ==========================================
print("\n=== 5. 最终入模 (Tensor) ===")

# 4.1 特征转 Float32
X_tensor = torch.tensor(X_scaled, dtype=torch.float32)

# 4.2 标签转 Float32 (二分类通常用 Float) 并调整形状
y_tensor = torch.tensor(y_numpy, dtype=torch.float32)

# ⚠️ 关键操作：把 y 从一行线 [0, 1, 0] 变成一根柱子 [[0], [1], [0]]
# 否则以后算 Loss 肯定报错
y_tensor = y_tensor.view(-1, 1)

print("最终训练数据 X_tensor:\n", X_tensor)
print("最终训练标签 y_tensor:\n", y_tensor)

print("\n✅ 数据处理流程结束，可以直接喂给神经网络了！")