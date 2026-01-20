# Water Industrial AI - Week 4 Practice

## 📖 项目介绍
这是一个工业 AI 算法应用的练习项目，主要模拟了水务场景下的**管道压力预测**与**自动化周报生成**流程。

通过本项目，我练习了以下技能：
- 使用 **XGBoost** 进行回归预测 (`train_pressure_xgb.py`)
- 数据的加载与预处理 (`db_loader.py`, `ts_db_loader.py`)
- 模型文件的保存与加载 (`pressure_xgb.pkl`)
- 自动化生成包含图表的数据分析报告 (`generate_report.py`)

## 📂 文件结构说明

```text
Week4/water_industrial_ai/
├── data/               # 数据处理层
│   ├── generate_data.py    # 生成模拟数据
│   └── db_loader.py        # 数据库加载工具
├── models/             # 模型层
│   ├── train_pressure_xgb.py # XGBoost 模型训练脚本
│   └── pressure_xgb.pkl      # 训练好的模型文件
├── reports/            # 报告输出层
│   ├── generate_report.py    # 报告生成脚本
│   └── weekly_report.png     # 自动化生成的周报图表
├── utils/              # 工具函数
├── fonts/              # 绘图字体文件 (SimHei)
└── main.py             # 程序主入口