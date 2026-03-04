import pandas as pd
import numpy as np
import os # <--- 引入 os 模块处理路径

print("=== 正在生成水厂传感器历史数据 ===")
# 固定随机种子，确保每次生成的数据一样
np.random.seed(42)

# 模拟 5000 条真实水质监控数据
num_samples = 5000

data_df = pd.DataFrame({
    'PH': np.random.uniform(6.5, 8.5, num_samples),         # 水厂常见 PH 范围
    'Turbidity': np.random.uniform(5.0, 40.0, num_samples), # 浊度 NTU
})

# 模拟真实的“综合水质得分”计算逻辑 (带有一些不可控的物理/化学噪音)
data_df['Quality_Score'] = 2.5 * data_df['PH'] - 0.8 * data_df['Turbidity'] + np.random.normal(0, 0.5, num_samples)

# ==========================================
# 🌟 路径魔法：确保文件保存在当前代码所在的文件夹
# ==========================================
# 1. 获取当前代码文件所在的文件夹路径
base_dir = os.path.dirname(os.path.abspath(__file__))

# 2. 把文件夹路径和文件名拼装在一起
csv_path = os.path.join(base_dir, 'beishui_sensor_data.csv')

# 3. 保存
data_df.to_csv(csv_path, index=False)

print(f"✅ 数据已成功保存到:\n{csv_path}")
print("\n前 5 行数据预览：")
print(data_df.head())