import pandas as pd
import numpy as np
import os
import math

print("=== 正在生成 30 天水压时序数据 ===")
# 1个月，每天 24 小时，每小时 60 分钟 = 43200 条数据
num_points = 30 * 24 * 60 
dates = pd.date_range(start='2023-10-01', periods=num_points, freq='1min')

# 模拟水压规律：基础水压 + 每日周期(正弦) + 随机白噪声
# 假设每天有两个用水高峰期，所以周期调一调
time_array = np.arange(num_points)
pressure = 0.5 + 0.15 * np.sin(2 * np.pi * time_array / (24 * 60)) \
               + 0.05 * np.sin(2 * np.pi * time_array / (12 * 60)) \
               + np.random.normal(0, 0.02, num_points)

df = pd.DataFrame({'time': dates, 'pressure': pressure})

# 确保 data 文件夹存在并保存
# 获取当前代码所在文件夹路径
base_dir = os.path.dirname(os.path.abspath(__file__))
# 将路径与保存文件的名字拼接
csv_path = os.path.join(base_dir, 'water_pressure_1month.csv')
# 开始保存
df.to_csv(csv_path, index=False)

print(f"✅ 生成完毕！共 {len(df)} 条数据。文件保存在: {csv_path}")