import pandas as pd

# 准备数据 (字典格式：Key是列名, Value是数据列表)
data = {
    '姓名': ['张三', '李四', '王五', '赵六'],
    '年龄': [23, 22, 25, 22],
    '城市': ['北京', '上海', '深圳', '北京'],
    '分数': [88.5, 92.0, 79.5, 95.0]
}

# 变成 DataFrame
df = pd.DataFrame(data) 
# 或者更常见的 pd.DataFraame(data)

print("--- 原始表格 ---")
print(df)