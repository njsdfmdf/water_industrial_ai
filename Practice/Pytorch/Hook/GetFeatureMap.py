import torch
import torchvision.models as models

# 1. 加载一个现成的预训练模型 (这里用 ResNet18 作为例子)
model = models.resnet18(pretrained=True)
# 为了测试，我们开启评估模式 (省电模式)
model.eval() 

# 2. 准备一个"空箱子"来装特征图
# 用字典比较好，可以给提取的特征图起个名字
features_loot = {}

# 3. 定义我们的 "小偷" (Hook 函数)
# PyTorch 规定，前向传播的 Hook 函数必须接收这三个固定的参数
def get_features_hook(name):
    def hook(module, input, output):
        # module: 当前这一层本身
        # input: 流进这一层的数据
        # output: 这一层计算完吐出的数据 (这就是我们要的特征图！)
        
        # 把 output 从计算图中剥离出来 (detach)，并不再跟踪梯度，然后存进箱子里
        # 作用于单个张量（Tensor）。当 output 从网络里出来时，它的屁股后面连着一根长长的线（计算图），顺着这根线能一路找回最开始的输入，用来算梯度。output.detach() 就是一剪刀把这根线剪断。拿走剪断后的数据，就不会影响原来的网络了。
        features_loot[name] = output.detach()
    return hook

# 4. 把小偷 "绑" 在你想偷窥的特定层上
# 假设我们想看 ResNet18 里的 layer1 的第一块 (一个卷积模块)
target_layer = model.layer1[0]

# register_forward_hook 会返回一个句柄 (handle)，我们可以用它来拆除钩子
hook_handle = target_layer.register_forward_hook(get_features_hook('layer1_output'))

print("✅ 钩子已成功挂载！")

# 5. 制造一张假的输入图片 (BatchSize=1, 通道=3, 高=224, 宽=224)
dummy_image = torch.randn(1, 3, 224, 224)

# 6. 正常让数据跑过模型，并不更新数据
with torch.no_grad():
    print("🚀 开始前向传播 (快递发车)...")
    final_output = model(dummy_image)

# 7. 检查我们的 "战利品"
print("\n--- 🕵️‍♂️ 检查偷取到的特征图 ---")
stolen_feature = features_loot['layer1_output']
print(f"偷到的数据类型: {type(stolen_feature)}")
print(f"偷到的特征图形状: {stolen_feature.shape}") 
# print(final_output)
# 预期形状大概是 [1, 64, 56, 56]，表示 64 张 56x56 的小图

# 8. 养成好习惯：用完拆除钩子，防止后面继续偷导致内存爆炸
hook_handle.remove()
print("\n🧹 钩子已拆除，清理现场完毕。")