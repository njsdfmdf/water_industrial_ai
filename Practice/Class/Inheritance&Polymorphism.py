from abc import ABC, abstractmethod  # 引入抽象基类库


# 1. 定义抽象基类 (Base Class)
# 这是一个契约，不能被直接实例化，只能被继承
class BaseTransformer(ABC):
    def __init__(self, column_name):
        self.column_name = column_name

    # @abstractmethod 强制子类必须重写这个方法，否则报错
    @abstractmethod
    def transform(self, data):
        pass

    def get_info(self):
        # 普通方法，子类可以直接用
        return f"处理器目标列: {self.column_name}"


# 2. 子类 A: 归一化处理器
class MinMaxTransformer(BaseTransformer):
    def transform(self, data):
        print(f"📉 [MinMax] 正在归一化列: {self.column_name}")
        # 模拟归一化逻辑: (x - min) / (max - min)
        return [x / 100.0 for x in data]


# 3. 子类 B: 对数处理器
class LogTransformer(BaseTransformer):
    def transform(self, data):
        print(f"📊 [Log] 正在进行对数变换列: {self.column_name}")
        # 模拟对数变换
        return ["log(" + str(x) + ")" for x in data]


# --- 多态演示 ---
# 定义一个通用的处理管道，它不关心具体是哪种 Transformer
def run_pipeline(transformers, raw_data):
    print("--- 开始执行流水线 ---")
    for tf in transformers:
        # 多态的核心：我们只调用 transform，具体执行哪个类的代码由对象类型决定
        print(tf.get_info())
        result = tf.transform(raw_data)
        print(f"结果: {result}\n")


# 实例化不同的子类
t1 = MinMaxTransformer("PH值")
t2 = LogTransformer("浊度")

# 放入列表，批量执行
run_pipeline([t1, t2], [10, 50, 90])
