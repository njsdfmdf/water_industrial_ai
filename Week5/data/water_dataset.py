import torch
from torch.utils.data import Dataset
import pandas as pd
import numpy as np

class WaterDataset(Dataset):
    def __init__(self, csv_file):
        """初始化：只读取文件名，不一次性加载所有图片(如果是图片任务)"""
        self.data = pd.read_csv(csv_file)

        # 假设我们要用 'pressure_lag_1', 'pressure_lag_2' 预测 'pressure'
        # 这里的列名要和你 CSV 里的一致
        self.features = self.data[['pressure_lag_1', 'pressure_lag_2']].values.astype(np.float32)
        self.labels = self.data['pressure'].values.astype(np.float32)

    def __len__(self):
        """告诉 PyTorch 数据集有多长"""
        return len(self.data)

    def __getitem__(self, idx):
        """告诉 PyTorch 怎么拿第 idx 条数据"""
        x = torch.from_numpy(self.features[idx])
        y = torch.tensor(self.labels[idx]) # 单个数值
        return x, y

# 测试代码 (一定要写！在本地测通了再上传)
if __name__ == "__main__":
    ds = WaterDataset('/home/xuepeng/code/Week5/data/train.csv')
    print(f"第一条数据: {ds[0]}")