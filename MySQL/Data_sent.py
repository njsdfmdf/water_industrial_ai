import pandas as pd
from sqlalchemy import create_engine

# 1. 连接配置
db_url = "mysql+pymysql://root:123456@localhost:3306/water_db"
engine = create_engine(db_url)

# 2. 读取 CSV 数据
# 假设 CSV 文件就在当前目录下
# pd.read_csv(...)：这相当于你把原件拿去复印了一份，这张复印件就是 df
df = pd.read_csv("predictive_maintenance.csv")

print("原始 CSV 列名:", df.columns.tolist())

# --- 关键步骤：列名映射 (对齐) ---
# 数据库里的字段名是固定的，但 CSV 里的表头可能是 "Air temperature [K]" 这种。
# 必须把 CSV 的列名改成和数据库一模一样！
# 格式：{'CSV里的旧名字': '数据库里的新名字'}
column_mapping = {
    "UDI": "udi",
    "Product ID": "product_id",
    "Type": "type",
    "Air temperature [K]": "air_temp",
    "Process temperature [K]": "process_temp",
    "Rotational speed [rpm]": "rot_speed",
    "Torque [Nm]": "torque",
    "Tool wear [min]": "tool_wear",
    "Target": "target",
    "Failure Type": "failure_type",
}

# 执行重命名，修改df中的.csv文件副本
# df.rename(...)：这相当于你拿着笔，在复印件（df）上把“Product ID”涂掉，改写成了“product_id”。
# # inplace=True 的意思是：直接在当前这张“复印件”上改，不要重新复印一张
df.rename(columns=column_mapping, inplace=True)

# 再次检查：只保留数据库里有的那些列，防止 CSV 里有多余的列报错
expected_columns = [
    "udi",
    "product_id",
    "type",
    "air_temp",
    "process_temp",
    "rot_speed",
    "torque",
    "tool_wear",
    "target",
    "failure_type",
]

# 筛选列（如果 CSV 里有 extra_column，这一步会自动丢弃它）
df = df[expected_columns]

print("修正后的列名:", df.columns.tolist())

# 3. 写入数据库
print("正在写入数据库...")
try:
    # to_sql：你把这张改好名字的复印件交给了数据库管理员（MySQL）。
    df.to_sql(
        name="device_maintenance",  # 必须和你建的表名一模一样
        con=engine,
        if_exists="append",  # 关键！因为表已经存在，我们要“追加”进去
        index=False,  # 不要把 Pandas 的索引 0,1,2 存进去
        chunksize=1000,  # 分批写入，更稳
    )
    print("✅ 成功写入 device_maintenance 表！")

except Exception as e:
    print(f"❌ 写入失败: {e}")
    print("提示：请检查是否有重复的主键 (udi)，或者数据类型不匹配。")
