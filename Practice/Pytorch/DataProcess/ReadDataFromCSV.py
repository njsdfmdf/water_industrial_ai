import torch
import pandas as pd
import numpy as np
import io

# --- 1. 模拟生成一个 CSV 文件 (实际工作中你会直接 pd.read_csv('data.csv')) ---
csv_content = """PH值,浊度,泵状态
7.2,15.5,On
6.8,20.1,Off
7.5,12.3,On
6.5,25.0,Off
7.0,18.2,On"""

# 读取 CSV (这里用 io.StringIO 模拟读取文件，实际你就写文件路径)
df = pd.read_csv(io.StringIO(csv_content))

print("=== 原始 Excel/CSV 数据 ===")
print(df)

# --- 2. 处理非数值列 (Categorical Data) ---
# 工业界常用方法：映射字典 (Mapping)
status_mapping = {'On': 1, 'Off': 0}

# 将 '泵状态' 列的文字替换成数字
df['泵状态'] = df['泵状态'].map(status_mapping)

print("\n=== 清洗后的全是数字的数据 ===")
print(df)

# --- 3. 分离特征 (Inputs) 和 标签 (Target) ---
# .values 会把 Pandas 表格变成 Numpy 数组
x_data = df[['PH值', '浊度']].values  # 取前两列作为输入
y_data = df['泵状态'].values         # 取最后一列作为目标

print(f"\n特征 (Numpy): \n{x_data}")
print(f"标签 (Numpy): {y_data}")

# --- 4. 转换为 Tensor ---
# ⚠️ 注意 dtype 的设置！这是新手通过率最低的坑
x_tensor = torch.tensor(x_data, dtype=torch.float32)
y_tensor = torch.tensor(y_data, dtype=torch.long)

print("\n=== 最终成品的 Tensor ===")
print("X (Features):")
print(x_tensor)
print(f"Shape: {x_tensor.shape}") # [5, 2] -> 5条数据，每条2个特征

print("\n y (Labels):")
print(y_tensor)
print(f"Shape: {y_tensor.shape}") # [5] -> 5个标签