import pandas as pd
from sqlalchemy import create_engine

# 1. 还是那个配置 (如果是远程，就把 localhost 改成 IP)
db_url = "mysql+pymysql://root:123456@localhost:3306/water_db"
engine = create_engine(db_url)

# 2. 写一句 SQL 查询语句
# 比如：我想把刚才存进去的数据全部取出来
sql = "SELECT * FROM water_pressure"

# 或者：只取压力大于 2.0 的异常数据
# sql = "SELECT * FROM water_pressure WHERE pressure > 2.0"

try:
    print("📥 正在从数据库提取数据...")

    # 3. 核心代码：一行搞定读取！
    # Pandas 会自动执行 SQL，把结果转换成 DataFrame
    df_result = pd.read_sql(sql, engine)

    print("✅ 提取成功！来看看前 5 行：")
    print(df_result.head())

    print(f"\n📊 数据统计：共提取了 {len(df_result)} 条数据")

except Exception as e:
    print(f"❌ 提取失败: {e}")
