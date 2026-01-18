import pandas as pd
from sqlalchemy import create_engine, text
import os

# 连接数据库
engine = create_engine("mysql+pymysql://root:123456@localhost:3306/water_db")


def get_clean_data(area_name):
    """
    拉取指定区域数据，并进行清洗
    """
    print(f"正在拉取 {area_name} 的数据...")
    
    # 1. 编写 SQL (使用参数化查询防止注入，虽然这里是内部使用)
    sql = f"""
    SELECT record_time, pressure 
    FROM water_pressure 
    WHERE area = '{area_name}' 
    AND record_time >= '2023-01-01'
    ORDER BY record_time
    """
    
    # 2. 读取数据
    with engine.connect() as conn:
        df = pd.read_sql(text(sql), conn)

    
    print(f"原始数据量: {len(df)}")
    
    # 3. 数据清洗
    # 3.1 处理缺失值：用前一个有效值填充 (fillna method='ffill')
    # 水压是连续变化的，用前一时刻的数据填充最合理
    df['pressure'] = df['pressure'].fillna(method='ffill') # ffill是Foward Fill，向前填充
    
    # 3.2 剔除异常值：简单粗暴法，剔除 > 2.0 的数据
    # 在工业中，这部分数据通常要单独拿出来报警，但在训练模型时要剔除
    df_clean = df[df['pressure'] <= 2.0] # 里面的列表生成一个满是True或是False的列表，并不返回数据，外面的列表根据这个True和False值保留数据
    

    print(f"清洗后数据量: {len(df_clean)}")
    print("前5条数据预览:")
    print(df_clean.head())
    
    return df_clean

if __name__ == "__main__":
    # 测试函数
    df_result = get_clean_data('A区')
    # 可以选择保存清洗后的数据
    # 只有一种情况你通过通常需要保留索引：当索引本身就是重要数据时可以写成index=True
    df_result.to_csv('cleaned_data_A.csv', index=False)
    print("清洗完成，文件已保存。")

    print("当前文件将会被保存到这里:", os.getcwd())