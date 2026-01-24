import os
import torch
import matplotlib.pyplot as plt


# randn 是 "Random Normal" 的缩写。

# 用统计学的术语来说，它生成的是服从 “标准正态分布” (Standard Normal Distribution) 的随机数。

# 设置这种呈正态分布的随机数可以保证训练顺利进行不会出现卡住的情况

x = torch.linspace(0, 1, 100).unsqueeze(1)
y = 2 * x + 0.5 + torch.randn(x.size()) * 0.5

w = torch.randn(1, 1, requires_grad=True)

b = torch.randn(1, 1, requires_grad=True)


learning_rate = 0.01

for epoch in range(100):
    y_pred = x.mm(w) + b
    loss = 0.5 * (y_pred - y).pow(2).mean()

    loss.backward()

    with torch.no_grad():
        w -= learning_rate * w.grad
        b -= learning_rate * b.grad

        w.grad.zero_()
        b.grad.zero_()

    if epoch % 10 == 0:
        print(f"Epoch {epoch}: Loss = {loss.item():.4f}")


print(f"训练结果: w={w.item():.2f}, b={b.item():.2f}")


# 画图看看拟合效果

plt.scatter(x.numpy(), y.numpy())
plt.plot(x.numpy(), y_pred.detach().numpy(), "r")

# 1.
curent_script_path = os.path.abspath(__file__)

models_dir = os.path.dirname(curent_script_path)

week5_dir = os.path.dirname(models_dir)

save_dir = os.path.join(week5_dir, 'reports')

print(f"Image will save to: {save_dir}")

if not os.path.exists(save_dir):
    os.makedirs(save_dir)

plt.savefig(f"{save_dir}/linear_fir_manul.png")
