import torch

# 1. 准备数据
x = torch.tensor([1.0])
target = torch.tensor([10.0])

# 2. 初始化参数 (随便猜一个数)
w = torch.tensor([2.0], requires_grad=True)
b = torch.tensor([0.0], requires_grad=True)

# 3. 设置超参数
lr = 0.05 # 学习率
epochs = 100 # 训练轮数 (循环100次)

print("=== 开始训练 ===")

for epoch in range(epochs):
    # A. 前向传播
    y_pred = w * x + b
    
    # B. 计算 Loss
    loss = (y_pred - target) ** 2
    
    # C. 反向传播 (算梯度)
    loss.backward()
    
    # D. 更新参数
    with torch.no_grad():
        w -= lr * w.grad
        b -= lr * b.grad
        
        # E. 梯度清零 (千万别忘了!)
        w.grad.zero_()
        b.grad.zero_()
    
    # 每隔 10 轮打印一次进度
    if epoch % 10 == 0:
        print(f"Epoch {epoch}: Loss = {loss.item():.4f}, w = {w.item():.4f}, b = {b.item():.4f}")

print("=== 训练结束 ===")
print(f"最终结果: w={w.item():.4f}, b={b.item():.4f}")
print(f"最终预测: {w * x + b}") 
# 你会发现结果非常接近 10.0