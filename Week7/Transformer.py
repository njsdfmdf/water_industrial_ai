import torch
import torch.nn as nn
import math
import numpy as np
import pandas as pd
from torch.utils.data import DataLoader, TensorDataset
from sklearn.preprocessing import StandardScaler
import os

# ==========================================
# 第一步：准备一个“打标签机”（位置编码）
# 这是硬核的数学部分，工业界通常直接抄这个标准模板，不用自己推导
# ==========================================
class PositionalEncoding(nn.Module):
    def __init__(self, d_model, max_len=5000):
        super(PositionalEncoding, self).__init__()
        # 创建一个足够长的位置编码矩阵
        pe = torch.zeros(max_len, d_model)
        position = torch.arange(0, max_len, dtype=torch.float).unsqueeze(1)
        div_term = torch.exp(torch.arange(0, d_model, 2).float() * (-math.log(10000.0) / d_model))
        # 用正弦和余弦函数生成周期性波动，作为时间戳
        pe[:, 0::2] = torch.sin(position * div_term)
        pe[:, 1::2] = torch.cos(position * div_term)
        pe = pe.unsqueeze(0) # 加上 batch 维度
        # 注册为 buffer，这样它就不会被优化器更新
        self.register_buffer('pe', pe)

    def forward(self, x):
        # 把时间戳加到输入数据上
        x = x + self.pe[:, :x.size(1)]
        return x

# ==========================================
# 第二步：搭建属于你的水压预测 Transformer
# ==========================================
class TimeSeriesTransformer(nn.Module):
    def __init__(self, input_size=1, d_model=64, nhead=4, num_layers=2, output_size=60, window_size=120):
        super().__init__()
        
        # 1. 扩容：把单纯的1个水压数值，映射成包含64个特征的高维空间 (d_model)
        self.input_linear = nn.Linear(input_size, d_model)
        
        # 2. 贴标签：注入位置编码
        self.pos_encoder = PositionalEncoding(d_model)
        
        # 3. 核心引擎：自注意力机制层 (Encoder)
        # batch_first=True 意思是输入数据的格式是 (批次大小, 时间步, 特征数)
        encoder_layer = nn.TransformerEncoderLayer(d_model=d_model, nhead=nhead, batch_first=True)
        self.transformer_encoder = nn.TransformerEncoder(encoder_layer, num_layers=num_layers)
        
        # 4. 输出层：把经过 Transformer 思考后的特征，压缩成我们需要预测的 60 个未来水压值
        self.fc = nn.Linear(window_size * d_model, output_size)

    def forward(self, x):
        # x 的原始形状: (batch_size, 120, 1)
        
        x = self.input_linear(x)        # 变成 (batch_size, 120, 64)
        x = self.pos_encoder(x)         # 加上位置信息
        
        # 经过注意力机制思考
        out = self.transformer_encoder(x) # 形状仍为 (batch_size, 120, 64)
        
        # 压扁它，准备输出
        out = out.reshape(out.shape[0], -1) # 变成 (batch_size, 120 * 64)
        
        # 输出 60 分钟的预测结果
        final_out = self.fc(out)          # 变成 (batch_size, 60)
        return final_out

# ==========================================
# 第三步：运行与训练 (复用你的数据和流程)
# ==========================================
def run():
    print("🚀 正在启动 Transformer 时序预测任务...")
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"当前使用的硬件设备: {device}")

    # --- 1. 加载和处理数据 (和你 LSTM 的逻辑一模一样) ---
    base_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(base_dir,'water_pressure_1month.csv') 
    
    if not os.path.exists(csv_path):
        print(f"❌ 找不到数据文件：{csv_path}。请确认 Day 1 的数据生成脚本已运行。")
        return

    df = pd.read_csv(csv_path)
    data = df['pressure'].values.reshape(-1, 1)

    split_idx = int(len(data) * 0.7)
    train_data = data[:split_idx]
    test_data = data[split_idx:]

    scaler = StandardScaler()
    train_scaled = scaler.fit_transform(train_data)
    test_scaled = scaler.transform(test_data)
    data_scaled = np.vstack((train_scaled, test_scaled))

    def create_sliding_window(dataset, window_size=120, predict_step=60):
        X, Y = [], []
        for i in range(len(dataset) - window_size - predict_step):
            X.append(dataset[i : i + window_size])
            Y.append(dataset[i + window_size : i + window_size + predict_step])
        return np.array(X), np.array(Y)

    X_all, Y_all = create_sliding_window(data_scaled, window_size=120, predict_step=60)
    train_size = split_idx - 120 - 60
    
    X_train_t = torch.tensor(X_all[:train_size], dtype=torch.float32)
    Y_train_t = torch.tensor(Y_all[:train_size], dtype=torch.float32).squeeze(-1)
    
    train_loader = DataLoader(TensorDataset(X_train_t, Y_train_t), batch_size=128, shuffle=True)

    # --- 2. 初始化 Transformer 模型 ---
    model = TimeSeriesTransformer().to(device)
    optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
    criterion = nn.MSELoss()

    # --- 3. 开始训练 ---
    print("🧠 开始训练 Transformer 模型...")
    epochs = 30
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
            print(f"Epoch: [{epoch+1:02d}/{epochs}], Loss: {total_loss/len(train_loader):.4f}")

    print("✅ Transformer 训练完成！")
    
    # 工业级保存习惯
    save_path = os.path.join(base_dir, 'transformer_model.pth')
    torch.save(model.state_dict(), save_path)
    print(f"💾 模型已保存至: {save_path}")

if __name__ == "__main__":
    run()