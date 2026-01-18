import pandas as pd
import numpy as np
from sqlalchemy import create_engine
import datetime

# 1. 配置数据库连接
# 格式: mysql+pymysql://用户名:密码@地址:端口/数据库名
db_url = "mysql+pymysql://root:123456@localhost:3306/water_db"
engine = create_engine(db_url)


# 2. 生成仿真数据
def generate_fake_data(num_rows=5000):
    print(f"正在生成 {num_rows} 条仿真数据...")

    # 生成时间序列 (过去7天，每2分钟一条)
    base_time = datetime.datetime(2023, 1, 1, 0, 0, 0)
    times = [base_time + datetime.timedelta(minutes=2 * i) for i in range(num_rows)]

    # 生成水压数据 (正弦波 + 随机噪声，模拟真实波动)
    # 正常水压在 0.3 - 0.8 MPa 之间
    pressures = (
        0.5
        + 0.2 * np.sin(np.linspace(0, 100, num_rows))
        + np.random.normal(0, 0.05, num_rows)
    )

    # 制造 2% 的缺失值 (NaN)，供后续练习清洗
    mask_null = np.random.choice([True, False], size=num_rows, p=[0.02, 0.98])
    pressures[mask_null] = np.nan

    # 制造 1% 的异常值 (比如水管爆裂导致压力瞬间飙升到 2.0)
    mask_outlier = np.random.choice([True, False], size=num_rows, p=[0.01, 0.99])
    pressures[mask_outlier] = 2.5

    # 生成区域
    areas = np.random.choice(["A区", "B区", "C区"], size=num_rows)

    # 创建 DataFrame
    df = pd.DataFrame({"record_time": times, "pressure": pressures, "area": areas})

    return df


# 3. 执行导入
if __name__ == "__main__":
    df = generate_fake_data()

    # 核心修正：使用 if_exists='append' 避免删除你建好的表
    # index=False 表示不把 pandas 的索引写入数据库
    try:
        df.to_sql("water_pressure", engine, if_exists="append", index=False)
        print("✅ 数据导入成功！")
    except Exception as e:
        print(f"❌ 导入失败: {e}")
        # 如果提示缺少库，请在终端运行: pip install pandas numpy sqlalchemy pymysql
