from ultralytics import YOLO
import os

def run():
    print("🚀 开始 YOLOv8 安全帽检测训练...")
    
    # 1. 魔法：获取当前脚本所在的绝对路径 (也就是 Week8 文件夹的路径)
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 2. 拼装出 data.yaml 的绝对路径
    yaml_path = os.path.join(base_dir, "datasets", "hard_hat", "data.yaml")
    
    # 检查 yaml 文件是否存在
    if not os.path.exists(yaml_path):
        print(f"❌ 找不到配置文件: {yaml_path}，请检查文件拖拽是否正确！")
        return
    
    print(f"📄 找到配置文件: {yaml_path}")
    
    # 3. 加载官方轻量级模型 yolov8n
    model = YOLO('yolov8n.pt') 
    
    # 4. 开始训练 (参数已经适配了 Colab 的 T4 GPU)
    results = model.train(
        data=yaml_path,
        epochs=50,
        batch=16,
        imgsz=640,
        lr0=0.001,
        patience=10, 
        project=os.path.join(base_dir, "runs", "detect"), # 训练结果将保存在 Week8/runs/detect 下
        name="water_safety_v1"
    )
    print("✅ 训练完成！")

if __name__ == '__main__':
    run()