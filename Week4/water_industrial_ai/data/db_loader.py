# data/db_loader.py

import pandas as pd
from sqlalchemy import create_engine, text

# 数据库配置（以后进阶了可以写到配置文件 config.yaml 里）
DB_URL = "mysql+pymysql://root:123456@localhost:3306/water_db"

def get_connection():
    """获取数据库连接引擎"""
    return create_engine(DB_URL)

def load_pressure_training_data():
    """
    专门为水压预测模型准备数据
    包含：读取 SQL -> 构造滞后特征 -> 清洗空值
    :return: 处理好的 DataFrame
    """
    print("   [DB Loader] 正在从数据库读取数据...")
    
    engine = get_connection()
    
    # 1. 编写 SQL (只取我们需要的数据)
    sql = "SELECT record_time, pressure FROM water_pressure WHERE area='A区' ORDER BY record_time"

    # 2. 读取数据
    try:
        with engine.connect() as conn:
            df = pd.read_sql(text(sql), conn)
    except Exception as e:
        print(f"   [DB Loader] ❌ 数据库连接失败: {e}")
        return None

    if df.empty:
        print("   [DB Loader] ⚠️ 警告: 查询结果为空")
        return None

    # 3. 特征工程 (Feature Engineering)
    # 注意：这些逻辑原本是在 model 文件里的，现在移到这里
    # 这样 model 文件拿到手的就是可以直接用的“干净数据”
    print("   [DB Loader] 正在进行特征构造...")
    df["hour"] = df["record_time"].dt.hour
    df["dayofweek"] = df["record_time"].dt.dayofweek
    
    # 构造滞后特征 (Lag Features)
    df["pressure_lag_1"] = df["pressure"].shift(1)
    df["pressure_lag_2"] = df["pressure"].shift(2)
    
    # 删除因为 shift 产生的空值
    df.dropna(inplace=True)
    
    print(f"   [DB Loader] ✅ 数据加载完成，共 {len(df)} 条样本")
    return df

if __name__ == "__main__":
    # 这是一个简单的测试，直接运行这个文件看看能不能拿到数据
    df = load_pressure_training_data()
    if df is not None:
        print(df.head())