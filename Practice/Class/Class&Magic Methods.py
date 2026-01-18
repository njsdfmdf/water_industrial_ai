import time


class AIModelWrapper:
    # 1. __init__: 初始化状态
    def __init__(self, model_name, version="v1.0"):
        """
        初始化模型配置。
        :param model_name: 模型名称
        :param version: 版本号
        """
        self.model_name = model_name  # 实例属性：属于在这个具体的对象
        self.version = version
        self.is_loaded = True
        print(f"🔧 [系统] 配置已创建: {self.model_name} ({self.version})")

    # 模拟加载模型权重的方法
    def load_weights(self):
        print(f"Cc 正在加载 {self.model_name} 的权重文件...")
        time.sleep(0.5)
        self.is_loaded = True
        print("✅ [系统] 权重加载完毕。")

    # 2. __call__: 定义核心行为
    def __call__(self, input_data):
        """
        允许使用 object(data) 的方式直接进行预测
        """
        if not self.is_loaded:
            raise RuntimeError("❌ 错误: 模型尚未加载，请先调用 load_weights()")

        print(f"🚀 [推理] 正在处理输入数据: {input_data}")
        # 模拟预测逻辑
        result = [x * 2 for x in input_data]
        return result


# --- 练习区 ---
# 1. 实例化 (触发 __init__)
my_model = AIModelWrapper("WaterQualityPredictor")

# 2. 调用方法
# my_model.load_weights()

# 3. 像函数一样调用对象 (触发 __call__)
# 这比写 my_model.predict([1, 2, 3]) 要优雅，且符合 AI 框架标准
prediction = my_model([1, 2, 3])
print(f"预测结果: {prediction}")
