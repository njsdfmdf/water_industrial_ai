import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
import pandas as pd
import numpy as np
import os

# ==========================================
# 🌟 路径魔法：获取当前代码所在的文件夹路径
# ==========================================
base_dir = os.path.dirname(os.path.abspath(__file__))

# 拼装要读取的 CSV 路径
csv_path = os.path.join(base_dir, 'beishui_sensor_data.csv')
# ==========================================
# Step 1: 从 CSV 文件读取数据
# ==========================================
if not os.path.exists(csv_path):
    raise FileNotFoundError(f"找不到文件 {csv_path}，请先运行生成数据的脚本！")

print("=== 1. 正在从 CSV 加载数据 ===")
df = pd.read_csv(csv_path)
print(f"数据加载成功！总计 {len(df)} 条记录。")

# ==========================================
# Step 2: 定义 Dataset (包含标准化逻辑)
# ==========================================
class WaterQualityDataset(Dataset):
    def __init__(self, dataframe):
        self.x_data = dataframe[['PH', 'Turbidity']].values.astype(np.float32)
        self.y_data = dataframe[['Quality_Score']].values.astype(np.float32)
        self.length = len(dataframe)

        # 计算并保存标尺 (均值和标准差)
        self.x_mean = self.x_data.mean(axis=0)
        self.x_std = self.x_data.std(axis=0)
        self.y_mean = self.y_data.mean(axis=0)
        self.y_std = self.y_data.std(axis=0)

        # 执行标准化
        self.x_data = (self.x_data - self.x_mean) / self.x_std
        self.y_data = (self.y_data - self.y_mean) / self.y_std

    def __getitem__(self, index):
        # 提取单条数据并转为 Tensor
        x_tensor = torch.tensor(self.x_data[index], dtype=torch.float32)
        y_tensor = torch.tensor(self.y_data[index], dtype=torch.float32)
        return x_tensor, y_tensor

    def __len__(self):
        return self.length

# 实例化 Dataset 和 DataLoader
dataset = WaterQualityDataset(df)
dataloader = DataLoader(dataset, batch_size=64, shuffle=True) # 增加 Batch Size 到 64

# ==========================================
# Step 3: 搭建模型与优化器
# ==========================================
print("\n=== 2. 初始化模型架构 ===")
model = nn.Linear(2, 1)
criterion = nn.MSELoss()
# 使用 Adam 优化器，在工业界比 SGD 更快更稳
optimizer = optim.Adam(model.parameters(), lr=0.05) 

# ==========================================
# Step 4: 开始训练
# ==========================================
print("\n=== 3. 开始模型训练 ===")
epochs = 15

for epoch in range(epochs):
    total_loss = 0
    
    for inputs, targets in dataloader:
        optimizer.zero_grad()
        outputs = model(inputs)
        loss = criterion(outputs, targets)
        loss.backward()
        optimizer.step()
        
        total_loss += loss.item()
    
    avg_loss = total_loss / len(dataloader)
    if (epoch + 1) % 3 == 0 or epoch == 0:
        print(f"Epoch [{epoch+1}/{epochs}] - Average Loss: {avg_loss:.4f}")

print("训练结束！")

# ==========================================
# Step 5: 🌟 终极操作 - 检查点打包与保存 🌟
# ==========================================
print("\n=== 4. 正在打包并保存模型 Checkpoint ===")

# 创建一个大字典，把模型状态和数据标尺全部装进去
checkpoint = {
    'model_state_dict': model.state_dict(),  # 模型的权重和偏置
    'x_mean': dataset.x_mean,                # 必须带上，否则预测时无法预处理输入
    'x_std': dataset.x_std,
    'y_mean': dataset.y_mean,                # 必须带上，否则预测后无法还原真实分数
    'y_std': dataset.y_std,
    'features': ['PH', 'Turbidity']          # 记录一下特征顺序，防止以后搞混
}

# 保存到硬盘
# 拼装你要保存的 .pth 文件的路径
save_path = os.path.join(base_dir,'water_quality_model_v1.pth')
torch.save(checkpoint, save_path)

print(f"✅ 模型及预处理参数已成功封装备份至: {save_path}")
print("你可以把这个 .pth 文件发送给后端开发团队进行上线部署了！")