from influxdb import InfluxDBClient
import pandas as pd
import numpy as np
import datetime

# 1. 连接 InfluxDB
client = InfluxDBClient(host="localhost", port=8086)
client.switch_database("water_iot")

# 2. 写入仿真数据
print("正在写入时序数据...")
json_body = []
base_time = datetime.datetime.utcnow()

for i in range(100):
    point = {
        "measurement": "pressure",  # 相当于表名
        "tags": {"area": "A区", "sensor_id": "S001"},
        "time": (base_time + datetime.timedelta(minutes=i)).isoformat(),
        "fields": {"value": 0.5 + np.random.random() * 0.1},  # 模拟水压
    }
    json_body.append(point)

# 批量写入
client.write_points(json_body)
print("写入完成！")

# 3. 查询并转为 DataFrame
# 需求：查询最近1小时的数据
result = client.query("SELECT * FROM pressure WHERE time > now() - 1h")
# 将生成器转换为列表再转 DataFrame
points = list(result.get_points())
df = pd.DataFrame(points)

# 转换时间列格式
df["time"] = pd.to_datetime(df["time"])
# 设置时间为索引，方便后续重采样
df.set_index("time", inplace=True)

print("从 InfluxDB 读取的数据预览:")
print(df.head())
