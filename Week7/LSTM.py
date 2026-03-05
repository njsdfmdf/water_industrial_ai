import pandas as pd
import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import DataLoader, TensorDataset
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import os

# ==========================================
# 1. 加载与预处理数据
# ==========================================
print("加载数据...")

# 获取当前代码的路径
base_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(base_dir, 'water_pressure_1month.csv')

df = pd.read_csv(csv_path)
data = df['pressure'].values.reshape(-1, 1) # 变成二维数组

# 按 7:3 拆分数据 (严禁打乱！)
split_idx = int(len(data) * 0.7)
train_data = data[:split_idx]
test_data = data[split_idx:]

# 🌟 关键修正：仅用训练集 fit(计算均值和方差)
scaler = StandardScaler()
train_scaled = scaler.fit_transform(train_data)
test_scaled = scaler.transform(test_data) # 测试集只能 transform

# 拼回一个完整数组供滑窗使用
data_scaled = np.vstack((train_scaled, test_scaled))

# ==========================================
# 2. 构造滑窗函数 (Sliding Window)
# ==========================================
def create_sliding_window(dataset, window_size=120, predict_step=60):
    X, Y = [], []
    for i in range(len(dataset) - window_size - predict_step):
        X.append(dataset[i : i + window_size])
        Y.append(dataset[i + window_size : i + window_size + predict_step])
    return np.array(X), np.array(Y)

print("构造滑窗样本...")
X_all, Y_all = create_sliding_window(data_scaled, window_size=120, predict_step=60)

# 把滑窗后的数据按原来的 split_idx 拆分 (需要减去滑窗损耗)
train_size = split_idx - 120 - 60
X_train, Y_train = X_all[:train_size], Y_all[:train_size]
X_test, Y_test = X_all[train_size:], Y_all[train_size:]

# 转为 PyTorch Tensor
X_train_t = torch.tensor(X_train, dtype=torch.float32)
Y_train_t = torch.tensor(Y_train, dtype=torch.float32).squeeze(-1) # Y 去掉最后一个维度
X_test_t = torch.tensor(X_test, dtype=torch.float32)
Y_test_t = torch.tensor(Y_test, dtype=torch.float32).squeeze(-1)

train_loader = DataLoader(TensorDataset(X_train_t, Y_train_t), batch_size=128, shuffle=True)

# ==========================================
# 3. 定义 LSTM 模型
# ==========================================
class PressureLSTM(nn.Module):
    def __init__(self, input_size=1, hidden_size=64, num_layers=2, output_size=60):
        super(PressureLSTM, self).__init__()
        # batch_first=True 非常重要，代表输入数据的维度是 (batch, seq, feature)
        self.lstm = nn.LSTM(input_size, hidden_size, num_layers, batch_first=True)
        self.fc = nn.Linear(hidden_size, output_size)

    def forward(self, x):
        # x shape: (batch_size, 120, 1)
        out, (hn, cn) = self.lstm(x)
        # out shape: (batch_size, 120, 64)
        # 我们只取最后一个时间步的输出 (out[:, -1, :]) 来预测未来
        final_out = self.fc(out[:, -1, :]) 
        # final_out shape: (batch_size, 60)
        return final_out

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = PressureLSTM().to(device)
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
criterion = nn.MSELoss()

# ==========================================
# 4. 模型训练
# ==========================================
print(f"开始训练，使用设备: {device}")
epochs = 30 # 先跑 30 个 Epoch 看看效果，100可能太久
for epoch in range(epochs):
    model.train()
    total_loss = 0
    for batch_x, batch_y in train_loader:
        batch_x, batch_y = batch_x.to(device), batch_y.to(device)
        optimizer.zero_grad()
        output = model(batch_x)
        loss = criterion(output, batch_y)
        loss.backward()
        optimizer.step()
        total_loss += loss.item()
    if (epoch+1) % 5 == 0:
        print(f"Epoch: {epoch+1:02d}, Loss: {total_loss/len(train_loader):.4f}")

# ==========================================
# 5. 评估与可视化
# ==========================================
model.eval()
with torch.no_grad():
    # 拿测试集的第一条数据来预测
    test_sample_x = X_test_t[0:1].to(device) # Shape: (1, 120, 1)
    true_y = Y_test_t[0].numpy()             # Shape: (60,)
    pred_y = model(test_sample_x).cpu().numpy().flatten() # Shape: (60,)

# 逆标准化 (把缩放后的数值变回真实的水压 MPa)
true_y_real = scaler.inverse_transform(true_y.reshape(-1, 1)).flatten()
pred_y_real = scaler.inverse_transform(pred_y.reshape(-1, 1)).flatten()

plt.figure(figsize=(10, 5))
plt.plot(true_y_real, label='Real Pressure')
plt.plot(pred_y_real, label='Predicted Pressure', linestyle='--')
plt.title('LSTM 预测未来 60 分钟水压对比')
plt.xlabel('Future Time Steps (Minutes)')
plt.ylabel('Pressure (MPa)')
plt.legend()
plt.show()

# 保存模型
base_dir = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(base_dir, 'pressure_lstm.pth')
torch.save(model.state_dict(), model_path)
print("✅ LSTM 模型训练完毕并保存！")