import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader # <--- 引入主角
import pandas as pd
import numpy as np
import io

# ==========================================
# Step 0: 准备模拟数据 (1000条水质数据)
# ==========================================
# 只要学会处理这1000条，处理100万条也是一样的逻辑
# 规律：y = 2 * x1 - 1 * x2 + 噪音
print("正在生成模拟数据...")
data_df = pd.DataFrame({
    # 生成均匀分布的1000个数字，范围在6到9之间
    'PH': np.random.uniform(6, 9, 1000),       # 特征1
    # 生成均匀分布的1000个数，范围在10到50之间
    'Turbidity': np.random.uniform(10, 50, 1000), # 特征2
})
# 生成标签 (真实规律 + 一点点噪音)
# 含义：生成正态分布（高斯分布）的随机数，也就是噪音
# 参数：均值(loc)=0，标准差(scale)=0.1，数量 1000。
#  现实世界的数据永远不可能是完美的 $y=kx+b$，总会有误差。加上噪音是为了模拟真实的传感器波动。

# np.random.randn：是**“套餐”**（标准正态分布）。出厂设置锁死为 均值=0，标准差=1
# np.random.normal：是**“单点”**（一般正态分布）。你可以随意定制均值和标准差
data_df['Quality_Score'] = 2 * data_df['PH'] - 1 * data_df['Turbidity'] + np.random.normal(0, 0.1, 1000)

print(f"数据生成完毕，形状: {data_df.shape}")
print(data_df.head(3)) # 打印前3行看看

# ==========================================
# Step 1: 定义 Dataset (核心！)
# ==========================================
# 必须继承 Dataset 类，并实现三个魔法方法
class WaterQualityDataset(Dataset):
    def __init__(self, dataframe):
        """
        初始化：把数据存下来，做一些预处理
        """
        # 1. 提取特征 (前两列) 和 标签 (最后一列)
        # 注意这里的双层中括号 [['Quality_Score']] ！！！
        # 在 Pandas 中，如果你用双层中括号 [[]] 去提取列，它返回的不再是 1 维的 Series，而是一个 2维的DataFrame
        self.x_data = dataframe[['PH', 'Turbidity']].values.astype(np.float32)
        self.y_data = dataframe[['Quality_Score']].values.astype(np.float32)
        
        # 2. 这里的长度就是数据的总数
        self.length = len(dataframe)

        # === 🌟 关键修复：数据标准化 ===
        # 计算均值和标准差 (axis=0 代表按列算)
        self.x_mean = self.x_data.mean(axis=0)
        self.x_std = self.x_data.std(axis=0)
        self.y_mean = self.y_data.mean(axis=0)
        self.y_std = self.y_data.std(axis=0)

        # 执行标准化公式：(x - mean) / std
        # 这样所有数据都会变成 0 附近的小数
        self.x_data = (self.x_data - self.x_mean) / self.x_std
        self.y_data = (self.y_data - self.y_mean) / self.y_std
        
        print(f"数据预处理完毕！")
        print(f"X mean: {self.x_mean}, std: {self.x_std}")

    def __getitem__(self, index):
        """
        最重要的方法！
        它告诉 PyTorch当我要取第 index 条数据时，你该怎么给我。
        """
        # 1. 取出第 index 行数据
        x = self.x_data[index]
        y = self.y_data[index]
        
        # 2. 转成 Tensor (必须是 float32)
        # 注意：这里我们返回的是一条数据，不是一个 Batch
        # Dataset.__getitem__ 的角色：只负责拿“一件”物品。
        # 它的任务非常单纯，就是根据 index，把单独的一条水质数据（比如 [0.5, -1.2]，这是一个 1 维向量）拿出来。
        # 它不需要关心 Batch，不需要关心模型，它就是一个老老实实搬砖的。
        # 所以这里绝不能加 []，即绝不能写成[x]或[y]，因为之后的DataLoader会自动添加[]
        x_tensor = torch.tensor(x, dtype=torch.float32)
        y_tensor = torch.tensor(y, dtype=torch.float32)
        
        return x_tensor, y_tensor

    def __len__(self):
        """告诉 PyTorch 数据集有多大"""
        return self.length

# 实例化 Dataset
dataset = WaterQualityDataset(data_df)
# 测试一下：取第 0 条数据看看
print(f"\n[测试 Dataset] 第0条数据: {dataset[0]}")


# ==========================================
# Step 2: 定义 DataLoader (运输队)
# ==========================================
# batch_size=32: 每次给模型喂 32 条数据
# shuffle=True:  每一轮训练(Epoch)开始前，把数据打乱 (非常重要！)
dataloader = DataLoader(dataset, batch_size=32, shuffle=True)

# 测试一下 DataLoader
first_batch = next(iter(dataloader))
# 你会发现形状变成了 [32, 2] 和 [32, 1]，这就是 Batch 的魔力
print(f"\n[测试 DataLoader] 一个 Batch 的特征形状: {first_batch[0].shape}") 


# ==========================================
# Step 3: 搭建简单模型 (Phase 3的内容)
# ==========================================
model = nn.Linear(2, 1) # 输入2个特征(PH, 浊度)，输出1个分数
criterion = nn.MSELoss()
optimizer = optim.SGD(model.parameters(), lr=0.001) # 学习率调小点

# ==========================================
# Step 4: 完整的训练循环 (加入 Batch 循环)
# ==========================================
print("\n=== 开始工业级 Batch 训练 ===")

for epoch in range(10): # 训练 10 轮
    total_loss = 0
    
    # --- 内层循环：遍历 DataLoader ---
    # 每次循环，DataLoader 会自动送来 32 条数据 (inputs, targets)
    # enumerate: Python 内置函数。它不仅返回数据 (inputs, targets)，还顺便返回当前的序号 batch_idx（第几批）。
    for batch_idx, (inputs, targets) in enumerate(dataloader):
        
        # 1. 梯度清零
        optimizer.zero_grad()
        
        # 2. 前向传播
        outputs = model(inputs)
        
        # 3. 计算 Loss
        loss = criterion(outputs, targets)
        
        # 4. 反向传播
        loss.backward()
        
        # 5. 更新参数
        optimizer.step()
        
        # 记录总误差
        total_loss += loss.item()
    
    # 打印这一轮的平均误差
    avg_loss = total_loss / len(dataloader)
    print(f"Epoch {epoch+1}: Average Loss = {avg_loss:.4f}")

print("\n训练结束！")

# ==========================================
# Step 5: 预测时的注意事项 (反标准化)
# ==========================================

# 拿第0条数据测试
# 注意：这里加了 dtype=torch.float32 防止之前的 Double/Float 报错
test_input = torch.tensor([dataset.x_data[0]], dtype=torch.float32) 
pred_scaled = model(test_input).item()

# 还原！
# pred_scaled 是数字，但 y_std 和 y_mean 是数组
# 所以算出来的 pred_real 也是个数组，比如 array([15.23])
pred_real = pred_scaled * dataset.y_std + dataset.y_mean

# 同理 target_real 也是个数组
target_real = dataset.y_data[0][0] * dataset.y_std + dataset.y_mean

print(f"\n[验证还原结果]")
# 🚨 修改点：加上 [0] 取出数组里的第一个元素
print(f"模型预测(还原后): {pred_real[0]:.4f}")
print(f"真实标签(还原后): {target_real[0]:.4f}")