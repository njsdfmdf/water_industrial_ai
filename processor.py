import pandas as pd
import numpy as np

class WaterDataProcessor:
    """
    水务数据处理类：封装了读取、清洗、特征转换的方法
    """
    def __init__(self, file_path):
        self.file_path = file_path
        self.data = None
        print(f"初始化处理器，目标文件: {self.file_path}")

    def load_data(self):
        """读取数据，处理基本的读取错误"""
        try:
            self.data = pd.read_csv(self.file_path)
            print(f"成功读取数据，共 {len(self.data)} 行")
            return self.data
        except FileNotFoundError:
            print("错误：文件未找到，请检查路径")
            return None

    def clean_data(self):
        """清洗数据：填充缺失值"""
        if self.data is not None:
            # 假设 'ph' 列有缺失，用均值填充
            if 'ph' in self.data.columns:
                mean_ph = self.data['ph'].mean()
                self.data['ph'] = self.data['ph'].fillna(mean_ph)
                print(f"缺失值填充完毕，pH均值: {mean_ph:.2f}")
            else:
                print("警告：未找到 'ph' 列")
        return self.data

    def get_stats(self):
        """获取统计信息"""
        if self.data is not None:
            return self.data.describe()
        return "无数据"

# --- 测试代码 (main block) ---
if __name__ == "__main__":
    # 你需要先创建一个 dummy.csv 文件来测试
    processor = WaterDataProcessor("dummy.csv")
    processor.load_data()
    processor.clean_data()
    print(processor.get_stats())