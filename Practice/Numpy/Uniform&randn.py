import numpy as np
import matplotlib.pyplot as plt

# 1. 生成数据
# 正态分布 (randn)
data_normal = np.random.randn(100000) 


# 含义：生成正态分布（高斯分布）的随机数，也就是噪音
# 参数：均值(loc)=0，标准差(scale)=0.1，数量 1000。
#  现实世界的数据永远不可能是完美的 $y=kx+b$，总会有误差。加上噪音是为了模拟真实的传感器波动。

# np.random.randn：是**“套餐”**（标准正态分布）。出厂设置锁死为 均值=0，标准差=1
# np.random.normal：是**“单点”**（一般正态分布）。你可以随意定制均值和标准差
data_normal2 = np.random.normal(0, 0.1, 1000)


# 均匀分布 (uniform), 范围设为 -3 到 3，为了和上面对比
data_uniform = np.random.uniform(low=-3, high=3, size=100000)

# 2. 画图
plt.figure(figsize=(12, 5))

# 画正态分布
plt.subplot(1, 2, 1)
plt.hist(data_normal, bins=100, color='blue', alpha=0.7)
plt.title('Normal Distribution (randn)\nLike a Bell 🔔')
plt.xlabel('Value')
plt.ylabel('Count')

# 画均匀分布
plt.subplot(1, 2, 2)
plt.hist(data_uniform, bins=100, color='green', alpha=0.7)
plt.title('Uniform Distribution (uniform)\nLike a Brick 🧱')
plt.xlabel('Value')
plt.ylabel('Count')

plt.show()