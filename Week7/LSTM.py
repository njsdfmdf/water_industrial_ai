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
# StandardScaler() 是一个“数据缩放器”，它利用标准差标准化的方法，把你的数据变成均值为 0，方差为 1 的标准正态分布
scaler = StandardScaler()

#为什么训练集和测试集用的方法不一样？
# 这是算法工程里的铁律：严防数据穿越（Data Leakage）！
# 假设你在预测明天的水压，你今天能知道明天水压的均值和方差吗？绝对不可能。测试集模拟的就是“未知的未来”。所以，你只能用训练集的数据去 fit（计算出历史的均值和方差），然后用这个“历史的尺子”，去 transform（转换）测试集的数据。如果你对测试集也用了 fit，等于模型提前“偷看”了未来数据的整体分布规律，考试成绩就会虚高，一上线部署就彻底崩盘

# fit (计算)： 像是在做统计。它会去计算当前塞给它的数据的均值（mu）和标准差（sigma），并把它死死记住。fit_transform： 顾名思义，就是边计算边转换，一步到位。
train_scaled = scaler.fit_transform(train_data)

# transform (转换)： 像是一个执行者。它拿着刚才记下来的 mu 和 sigma，代入上面的公式，把数据替换成新的缩放值。
test_scaled = scaler.transform(test_data) # 测试集只能 transform

# 拼回一个完整数组供滑窗使用
data_scaled = np.vstack((train_scaled, test_scaled))

# ==========================================
# 2. 构造滑窗函数 (Sliding Window)
# ==========================================
# 为了生成 1个 完整的样本，你需要一口气消耗 120 + 60 = 180 个连续的数据点
# 当你的游标 i 滑动到最后时，必须要保证它后面还有 180 个空位让你截取
def create_sliding_window(dataset, window_size=120, predict_step=60):
    X, Y = [], []
    for i in range(len(dataset) - window_size - predict_step):
        X.append(dataset[i : i + window_size])
        Y.append(dataset[i + window_size : i + window_size + predict_step])
    return np.array(X), np.array(Y)

print("构造滑窗样本...")
X_all, Y_all = create_sliding_window(data_scaled, window_size=120, predict_step=60)

# 把滑窗后的数据按原来的 split_idx 拆分 (需要减去滑窗损耗)
# 由于模型需要往后探出 120 + 60 = 180 个身位 去凑齐一个完整的 (输入, 答案) 对。为了保证这 180 个身位不越过 split_idx 这条红线跑到测试集里去，能够用来生成训练样本的有效起点，自然就少了 180 个
train_size = split_idx - 120 - 60
X_train, Y_train = X_all[:train_size], Y_all[:train_size]
X_test, Y_test = X_all[train_size:], Y_all[train_size:]

# 转为 PyTorch Tensor
X_train_t = torch.tensor(X_train, dtype=torch.float32)
Y_train_t = torch.tensor(Y_train, dtype=torch.float32).squeeze(-1) # Y 去掉最后一个维度
X_test_t = torch.tensor(X_test, dtype=torch.float32)
Y_test_t = torch.tensor(Y_test, dtype=torch.float32).squeeze(-1)

# TensorDataset： 这是一个官方帮你写好的子类。就像是速食面。当你手头的数据已经是干净整齐的 PyTorch Tensor（比如我们这里的 X_train_t 和 Y_train_t），你直接把它们塞进 TensorDataset 里，它在底层自动帮你实现了 __len__ 和 __getitem__。省去了你写一堆模板代码的麻烦。
train_loader = DataLoader(TensorDataset(X_train_t, Y_train_t), batch_size=128, shuffle=True)

# ==========================================
# 3. 定义 LSTM 模型
# ==========================================
class PressureLSTM(nn.Module):
    def __init__(self, input_size=1, hidden_size=64, num_layers=2, output_size=60):
        super().__init__()
        # batch_first=True 非常重要，代表输入数据的维度是 (batch_size, sequence_length, input_size)
        # batch_size = 128（批次大小）：DataLoader 一次性发给显卡 128 个题目。
        # sequence_length = 120（序列长度）：每一道题里，包含了 120 个连续的时间点（120分钟的历史水压）。
        # input_size = 1（特征数）：在每一个时间点上，我们只记录了 1 个数值（水压）。如果你的数据源更丰富，比如同时记录了“水压”和“水管温度”，那这里就会变成 2。
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
# 把你建好的 LSTM 模型（加工厂的流水线），整个搬到了**显卡（GPU）**上
model = PressureLSTM().to(device)
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
criterion = nn.MSELoss()

# ==========================================
# 4. 模型训练
# ==========================================
print(f"开始训练，使用设备: {device}")
epochs = 30 # 先跑 30 个 Epoch 看看效果，100可能太久，Epoch = 1：代表模型把所有的训练数据，完完整整地看了一遍，epochs=30代表把训练集里的数据使用了30遍
for epoch in range(epochs):
    model.train()
    total_loss = 0
    # rain_loader（发牌员）从硬盘上读取数据打包成 batch_x 和 batch_y 时，这些数据默认是存放在**普通内存（CPU 领地）**里的
    for batch_x, batch_y in train_loader:
        # 把内存（CPU）里的数据原材料，用叉车搬运到显卡（GPU）的超高速加工厂里
        # PyTorch 的铁律：模型和数据必须在同一个物理设备上！
        # .to() 方法不是原地修改（In-place）的。它其实是把 CPU 里的数据复制了一份，然后发送到显卡上，并返回这个全新显卡张量的“引用地址”。如果你不把这个新的地址重新赋值给变量 batch_x，那你后续代码里用的 batch_x 依然是留在 CPU 里的那份老数据，依然会报错
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
    # test_sample_x.to(device)：先把 120 分钟的原始数据用卡车拉进 GPU
    test_sample_x = X_test_t[0:1].to(device) # Shape: (1, 120, 1)
    # 画图工具 matplotlib 是个“土老帽”，它只认识 CPU 里的 NumPy 数组，根本不认识 GPU 里的张量
    true_y = Y_test_t[0].numpy()             # Shape: (60,)

    # model(...)：GPU 里的模型飞速运转，吐出了预测结果。此时，这个结果依然被困在 GPU 显存里。
    # .cpu()：核心动作！ 用卡车把这个预测结果从 GPU 拉回普通内存（CPU）。
    # .numpy()：把 PyTorch 张量脱掉外衣，换上 matplotlib 认识的 NumPy 数组制服
    pred_y = model(test_sample_x).cpu().numpy().flatten() # Shape: (60,)

# 逆标准化 (把缩放后的数值变回真实的水压 MPa)
true_y_real = scaler.inverse_transform(true_y.reshape(-1, 1)).flatten()
pred_y_real = scaler.inverse_transform(pred_y.reshape(-1, 1)).flatten()

plt.figure(figsize=(10, 5))
plt.plot(true_y_real, label='Real Pressure', color='blue')
plt.plot(pred_y_real, label='Predicted Pressure', color='red', linestyle='--')

# 换成英文标题，彻底避开 Colab 中文乱码的坑
plt.title('LSTM Water Pressure Prediction (Next 60 mins)')
plt.xlabel('Future Time Steps (Minutes)')
plt.ylabel('Pressure (MPa)')
plt.legend()

# 🌟 核心杀招：强制保存到硬盘
plt.tight_layout()
plt.savefig('lstm_prediction_result.png', dpi=300)
print("✅ 图片已成功保存为：lstm_prediction_result.png")

plt.show() # 尝试在网页显示