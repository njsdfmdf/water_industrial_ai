import pandas as pd
import numpy as np
from sqlalchemy import create_engine, text
from sklearn.model_selection import train_test_split
import os

def run():
    """
    从 MySQL 读取数据 -> 构造特征 -> 导出为 train.csv 和 test.csv
    供 Colab 云端训练使用
    """
    print("   [Data Export] 🚀 正在启动数据导出流程...")

    # --- 1. 连接数据库 ---
    # 复用之前的连接逻辑
    db_url = "mysql+pymysql://root:123456@localhost:3306/water_db"
    try:
        engine = create_engine(db_url)
        # 测试连接
        with engine.connect() as conn:
            pass
    except Exception as e:
        print(f"   [Data Export] ❌ 数据库连接失败: {e}")
        print("   请检查 MySQL 服务是否开启 (sudo service mysql start)")
        return False

    # --- 2. 读取数据 ---
    # 模拟场景：只取 A 区的数据进行训练，一定要按时间排序！
    sql = """
        SELECT record_time, pressure 
        FROM water_pressure 
        WHERE area='A区' 
        ORDER BY record_time
    """
    
    print("   [Data Export] 正在读取数据...")
    try:
        with engine.connect() as conn:
            df = pd.read_sql(text(sql), conn)
    except Exception as e:
        print(f"   [Data Export] ❌ 读取数据出错: {e}")
        return False

    if df.empty:
        print("   [Data Export] ⚠️ 警告：数据库是空的！请先运行 data/generate_data.py")
        return False

    # --- 3. 特征工程 (关键步骤) ---
    # 这一步必须在这里做！因为 Colab 不连数据库，它只认 CSV 里的现成特征。
    print("   [Data Export] 正在构造 Lag 特征...")
    
    # 构造 T-1 和 T-2 时刻的水压特征
    df['pressure_lag_1'] = df['pressure'].shift(1)
    df['pressure_lag_2'] = df['pressure'].shift(2)
    
    # 刚才生成的 lag 特征会产生前两行空值，必须删掉，否则训练报错
    df.dropna(inplace=True)

    # --- 4. 划分训练集与测试集 ---
    # 时序数据严禁打乱顺序 (shuffle=False)，必须用过去预测未来
    print("   [Data Export] 正在切分数据集 (8:2)...")
    train_df, test_df = train_test_split(df, test_size=0.2, shuffle=False)

    # --- 5. 导出 CSV ---
    # 确保保存路径存在
    current_script_path = os.path.abspath(__file__)

    data_dir = os.path.dirname(current_script_path)

    save_dir = data_dir
    
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    train_path = os.path.join(save_dir, "train.csv")
    test_path = os.path.join(save_dir, "test.csv")

    # index=False 很重要，我们不需要 pandas 自动生成的 0,1,2... 索引列
    train_df.to_csv(train_path, index=False)
    test_df.to_csv(test_path, index=False)

    print(f"   [Data Export] ✅ 导出成功！")
    print(f"       Ref: 训练集保存至 -> {train_path} (共 {len(train_df)} 条)")
    print(f"       Ref: 测试集保存至 -> {test_path} (共 {len(test_df)} 条)")
    
    return True

if __name__ == "__main__":
    run()