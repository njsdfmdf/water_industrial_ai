import torch


# 一。定义数据
# === 1. 普通 Tensor (不可训练，比如输入数据 X) ===

x = torch.tensor([1.0], requires_grad=False) 
target = torch.tensor([10.0])

# 注意：在工业界，输入数据 X 不需要求导，因为我们不能修改数据本身！

# === 2. 权重 Tensor (可训练，比如参数 w) ===
# 假设公式是：y = w * x + b
# 我们希望 PyTorch 帮我们需要调整 w 和 b 来让结果更准
w = torch.tensor([2.0], requires_grad=True) 
b = torch.tensor([0.0], requires_grad=True)

print(f"w 的梯度功能开启了吗？ {w.requires_grad}")

# 开始训练
# === 3. 前向传播 (Forward Pass) ===
# 这就是一次预测过程
y_pred = w * x + b 

print(f"预测结果: {y_pred}")
# 输出: tensor([2.], grad_fn=<AddBackward0>)
# 注意那个 grad_fn！它就是“账本”，记录了y_pred是由加法运算(Add)得到的。

# 计算损失
loss = (y_pred - target) ** 2

print(f"当前 Loss: {loss.item()}") 
# (2 - 10)^2 = 64.0，误差很大！

# === 4. 反向传播 (Backward) —— 关键时刻！ ===
# 这一行代码执行后，PyTorch 会沿着计算图从 Loss 往回跑
# 算出 Loss 对 w 和 b 的偏导数（梯度）
loss.backward()

print("--- 查账结束 ---")


# 查看 w 的梯度 (dL/dw)
print(f"w 的梯度 (w.grad): {w.grad}")
# 数学推导: Loss = (wx + b - y)^2
# dL/dw = 2 * (wx + b - y) * x 
#       = 2 * (2*1 + 0 - 10) * 1 
#       = 2 * (-8) * 1 = -16
# 这里的 -16 意思是：如果你把 w 增加 1，Loss 会减少 16。
# 这说明 w 现在的 2.0 太小了，需要大幅增加！

# 查看 b 的梯度 (dL/db)
print(f"b 的梯度 (b.grad): {b.grad}")
# dL/db = 2 * (wx + b - y) * 1 = -16

# 查看 x 的梯度
print(f"x 的梯度: {x.grad}")
# 输出 None。因为 x 没开 requires_grad=True。
# 这也符合逻辑：我们要调整的是模型参数，不是篡改原始数据！

# 学习率 (Learning Rate)：控制每次修改的幅度，防止步子太大扯着蛋
lr = 0.01 

# 更新参数公式：w_new = w_old - lr * gradient
# (为什么要减？因为梯度指向 Loss 增加的方向，我们要去 Loss 减少的方向)

# ⚠️ 注意：更新参数时，必须告诉 PyTorch “这段代码别记账”
# 否则它会把“更新参数”这个动作也算进计算图里，导致无限套娃
with torch.no_grad():
    w -= lr * w.grad
    b -= lr * b.grad
    
    # 工业界必须做的操作：梯度清零！
    # 如果不清零，下一次 backward 算出来的梯度会和这次的累加，导致错误
    w.grad.zero_()
    b.grad.zero_()

print(f"学习后的新 w: {w}") # 应该比 2.0 大 (变成了 2.16)
print(f"学习后的新 b: {b}") # 应该比 0.0 大 (变成了 0.16)110