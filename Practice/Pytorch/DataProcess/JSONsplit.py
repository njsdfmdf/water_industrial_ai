import json
import pandas as pd
import io
import torch

# === 1. 模拟数据：在 CSV 里增加了 "Pump_Status" (0和1) ===
api_request_str = """
{
    "station_id": "Bj_Water_01",
    "data_format": "csv",
    "content": "PH,Turbidity,Pump_Status\\n7.2,15.5,1\\n6.8,20.1,0\\n7.5,12.3,1"
}
"""

# === 2. JSON 解包 ===
request_dict = json.loads(api_request_str)
csv_content = request_dict['content']

# === 3. Pandas 读取 (得到一张完整的包含答案的表) ===
df = pd.read_csv(io.StringIO(csv_content))
print("=== 完整数据表 ===")
print(df)

# === 4. 关键步骤：分离特征 (X) 和 标签 (y) ===

# 方式 A：按列名分离 (推荐，语义清晰)
# drop 会删除指定列，剩下的就是特征
feature_df = df.drop('Pump_Status', axis=1) 
# 单独取出这一列作为标签
label_df = df['Pump_Status']

# 方式 B：按位置切片 (iloc) - 适合老手
# feature_df = df.iloc[:, :-1] # 取所有行，取除了最后一列的所有列
# label_df = df.iloc[:, -1]    # 取所有行，只取最后一列

print("\n--- 分离结果 ---")
print("特征 (X):\n", feature_df.values)
print("标签 (y):\n", label_df.values)

# === 5. 转换为 Tensor (注意数据类型！) ===

# 特征通常必须是 float32
x_tensor = torch.tensor(feature_df.values, dtype=torch.float32)

# 标签的数据类型取决于你的任务：
# - 如果是二分类问题 (0/1)，通常用 float32 (配合 BCEWithLogitsLoss) 
# - 或者用 long (配合 CrossEntropyLoss)
# 这里我们先转为 float32
y_tensor = torch.tensor(label_df.values, dtype=torch.float32)

# 为了后续计算方便，标签通常需要 reshape 成 (N, 1) 的形状
y_tensor = y_tensor.view(-1, 1)

print("\n=== 最终 Tensor ===")
print(f"X shape: {x_tensor.shape}") # [3, 2] -> 3条数据，每条2个特征
print(f"y shape: {y_tensor.shape}") # [3, 1] -> 3个答案
print(y_tensor)