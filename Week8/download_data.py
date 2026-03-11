from roboflow import Roboflow
import os

print("🚀 正在下载 YOLO 格式的硬质安全帽数据集...")
# 使用公开的学术 API Key 临时下载
rf = Roboflow(api_key="i6L5SShCGICpZktb1unM") 
project = rf.workspace("joseph-nelson").project("hard-hat-workers")
version = project.version(14)

# 获得当前代码的路径
base_path = os.path.dirname(os.path.abspath(__file__))

# 拼接出最终的保存路径
save_path = os.path.join(base_path, "datasets", "hard_hat")

# --- 追踪代码开始 ---
print(f"📍 报告！当前脚本文件所在的绝对路径是: {base_path}")
print(f"🎯 报告！我正准备把数据存放到这里: {save_path}")
# --- 追踪代码结束 ---

os.makedirs(save_path, exist_ok=True)

# 下载到 datasets/hard_hat 目录
os.makedirs(save_path, exist_ok=True)
dataset = version.download("yolov8", location=save_path)
print("✅ 数据集下载并解压完成！")


                