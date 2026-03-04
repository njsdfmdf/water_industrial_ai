import torch
import torch.nn as nn # 神经网络模块
import torch.optim as optim # 优化器模块

# ==========================================
# Step 1: 搭建模型 (继承 nn.Module)
# ==========================================
class LinearModel(nn.Module):
    def __init__(self):
        super().__init__()
        # 定义一层线性网络: y = wx + b
        # in_features=1: 输入特征有1个
        # out_features=1: 输出特征有1个
        # PyTorch 会自动在这里面创建 w 和 b，并随机初始化
        
        # nn.Linear 和整个 PyTorch 框架设计的初衷就是为了批量处理数据。
        # 你定义的模型 nn.Linear(1, 1) 意思是：每个样本有 1 个特征进，1 个特征出。

        # 它并不关心你一次喂给它 1 个样本还是 100 个样本（Batch Size）
        self.linear = nn.Linear(in_features=1, out_features=1)

    def forward(self, x):
        # 定义前向传播路径
        return self.linear(x)

# 实例化模型
model = LinearModel()

# ==========================================
# Step 2: 定义 损失函数 和 优化器
# ==========================================
# MSELoss: 均方误差 (就是我们之前手写的 (y-y_hat)^2)
criterion = nn.MSELoss() 

# SGD: 随机梯度下降 (就是帮你做 w -= lr * grad 的工具人)
# model.parameters(): 告诉优化器，“请帮我管理这个模型里的所有 w 和 b”
optimizer = optim.SGD(model.parameters(), lr=0.05)

# ==========================================
# Step 3: 准备数据 (注意形状！)
# ==========================================
# 工业界标准：输入通常是矩阵 (Batch_Size, Features)
# 这里是 1条数据，1个特征 -> (1, 1)
# x = torch.tensor([[1.0]]) 
# target = torch.tensor([[10.0]])

# 修改后的数据：
# 我们构造一个 (3行, 1列) 的矩阵
# 代表 Batch_Size = 3, Feature_Dim = 1
x = torch.tensor([[1.0], [2.0], [3.0]]) 

# 目标也必须对应是 (3行, 1列)
target = torch.tensor([[2.0], [4.0], [6.0]])

# ==========================================
# Step 4: 训练循环 (The Loop)
# ==========================================
print("=== 使用 nn.Module 训练 ===")
for epoch in range(100):
    # 1. 梯度清零 (优化器的标准动作)
    # 等同于 w.grad.zero_()
    optimizer.zero_grad()
    
    # 2. 前向传播
    # PyTorch 的父类 nn.Module 内部帮你实现了 __call__ 方法。当你写 model(x) 时，Python 解释器其实是在后台默默执行了 model.__call__(x)。
    y_pred = model(x)
    
    # 3. 计算 Loss
    loss = criterion(y_pred, target)
    
    # 4. 反向传播
    loss.backward()
    
    # 5. 更新参数 (一步到位！)
    # 等同于 w -= lr * grad
    optimizer.step()

    if epoch % 20 == 0:
        # item() 取出数值
        print(f"Epoch {epoch}: Loss = {loss.item():.4f}")

# ==========================================
# Step 5: 验证结果
# ==========================================
# 打印模型内部自动生成的 w 和 b
for name, param in model.named_parameters():
    print(f"参数 {name}: {param.item():.4f}")


print(f"最终预测: {model(x)}")