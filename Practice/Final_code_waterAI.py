import pandas as pd
import numpy as np
from abc import ABC, abstractmethod
import functools


# ====================
# 1. 工具箱 (装饰器)
# ====================
def validate_input(func):
    @functools.wraps(func)
    def wrapper(self, df, *args, **kwargs):
        if df is None or df.empty:
            raise ValueError(f"❌ [{func.__name__}] 错误: 输入数据为空！")
        return func(self, df, *args, **kwargs)

    return wrapper


# ====================
# 2. 架构层 (抽象基类)
# ====================
class BaseProcessor(ABC):
    def __init__(self, source_path):
        self.source_path = source_path
        self.data = None
        print(f"🏗️ [{self.__class__.__name__}] 处理器初始化完成。源: {source_path}")

    @abstractmethod
    def load(self):
        pass

    @abstractmethod
    def process(self):
        pass


# ====================
# 3. 业务层 (具体实现)
# ====================
class WaterDataProcessor(BaseProcessor):
    def __init__(self, source_path, fill_value=0.0):
        # 调用父类初始化
        super().__init__(source_path)
        self.fill_value = fill_value

    def load(self):
        print(f"📂 正在读取数据: {self.source_path}")
        # 模拟数据读取
        # 实际开发中用: self.data = pd.read_csv(self.source_path)
        self.data = pd.DataFrame(
            {
                "PH": [7.1, 7.2, np.nan, 8.0, 7.1],
                "Turbidity": [0.5, 0.8, 1.2, np.nan, 105.0],  # 105.0 是异常值
            }
        )
        print("📊 原始数据预览:\n", self.data.head(), "\n")

    @validate_input  # <--- 使用装饰器确保数据安全
    def clean_na(self, df):
        print("🧹 [清洗] 正在填充缺失值...")
        return df.fillna(self.fill_value)

    @validate_input
    def filter_outliers(self, df):
        print("🔍 [过滤] 正在去除浊度异常值 (>100)...")
        # 假设浊度超过 100 为传感器故障
        return df[df["Turbidity"] < 100]

    def process(self):
        """实现基类要求的核心处理逻辑"""
        if self.data is None:
            self.load()

        # 链式处理
        df = self.clean_na(self.data)
        df = self.filter_outliers(df)

        self.data = df  # 更新内部状态
        return self.data

    # --- 魔术方法: 让实例可调用 ---
    def __call__(self):
        print("🚀 === 启动数据处理流水线 ===")
        return self.process()


# ====================
# 4. 运行验证
# ====================

# 实例化
processor = WaterDataProcessor(source_path="./data/2025_water.csv", fill_value=7.0)

# 执行 (像函数一样调用)
final_data = processor()

print("\n✅ 最终处理结果:")
print(final_data)
