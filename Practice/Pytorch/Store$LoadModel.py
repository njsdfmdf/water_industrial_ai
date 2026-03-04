import torch
import torch.nn as nn
import numpy as np


#-------------------上半场：训练环境 (算法工程师的工作)--------------
# 假设这是你训练好的模型
model = nn.Linear(2, 1)

# 假设这些是你从 Dataset 里算出来的标准化参数 (也就是我们在 Phase 4 算出来的那4个数)
# 注意：保存前最好确保它们是纯数值或 numpy array，或者是 Tensor
x_mean_val = np.array([7.5, 30.0], dtype=np.float32) # [PH均值, 浊度均值]
x_std_val = np.array([1.2, 15.0], dtype=np.float32)
y_mean_val = np.array([80.0], dtype=np.float32)      # 得分均值
y_std_val = np.array([5.0], dtype=np.float32)

# ==========================================
# 🌟 核心操作：创建一个“大字典” (Checkpoint)
# ==========================================
checkpoint = {
    # 1. 存模型的“秘方”
    'model_state_dict': model.state_dict(),
    
    # 2. 存数据的“标尺”
    'x_mean': x_mean_val,
    'x_std': x_std_val,
    'y_mean': y_mean_val,
    'y_std': y_std_val,
    
    # 你甚至可以存一些额外信息，方便日后追溯
    'info': '北水云服 v1.0 水质预测模型',
    'input_features': ['PH', 'Turbidity']
}

# 将这个大字典保存到硬盘
torch.save(checkpoint, 'water_quality_checkpoint.pth')
print("✅ 包含所有参数的大包裹已成功保存！")


# -------------下半场：生产环境 (后端/部署工程师的工作)--------

# 1. 后端同事先搭一个空壳模型
deploy_model = nn.Linear(2, 1)

# ==========================================
# 🌟 核心操作：读取“大字典”并拆包
# ==========================================
# 读取刚才保存的文件
loaded_checkpoint = torch.load('water_quality_checkpoint.pth')

# 拆包 1：把模型秘方装进去
deploy_model.load_state_dict(loaded_checkpoint['model_state_dict'])

# 拆包 2：把标准化参数拿出来
loaded_x_mean = loaded_checkpoint['x_mean']
loaded_x_std = loaded_checkpoint['x_std']
loaded_y_mean = loaded_checkpoint['y_mean']
loaded_y_std = loaded_checkpoint['y_std']

print(f"📦 拆包完成！加载的模型版本: {loaded_checkpoint['info']}")

# ==========================================
# 🚀 真实业务流：接收新数据并预测
# ==========================================
deploy_model.eval() # 开启评估模式

# 假设水厂传感器刚刚传来了最新的真实数据：PH=7.2, 浊度=25.0
raw_sensor_data = [7.2, 25.0]

# 🚨 步骤 A：用之前存下来的标尺，对新数据进行标准化！
# 公式：(x - mean) / std
scaled_input = (raw_sensor_data - loaded_x_mean) / loaded_x_std

# 转成 Tensor 并变成矩阵形状 (1, 2)
input_tensor = torch.tensor([scaled_input], dtype=torch.float32)

# 🚨 步骤 B：放入模型进行预测 (记得关闭梯度)
with torch.no_grad():
    scaled_prediction = deploy_model(input_tensor).item()

# 🚨 步骤 C：把模型输出的“缩放值”，还原成真实的“水质得分”
# 公式：y_pred * std + mean
final_real_score = scaled_prediction * loaded_y_std[0] + loaded_y_mean[0]

print(f"💧 传感器原始数据: PH={raw_sensor_data[0]}, 浊度={raw_sensor_data[1]}")
print(f"📈 最终预测水质得分: {final_real_score:.2f}")