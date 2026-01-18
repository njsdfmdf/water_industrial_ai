import pandas as pd
import numpy as np
import joblib
from sqlalchemy import create_engine, text
from xgboost import XGBRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.model_selection import train_test_split, GridSearchCV

# --- 1. 从 MySQL 取数 (复用第二周的成果) ---
print("正在从数据库读取数据...")
# 请替换为你的真实数据库连接
engine = create_engine("mysql+pymysql://root:123456@localhost:3306/water_db")

sql = f"""
    SELECT record_time, pressure FROM water_pressure WHERE area='A区' ORDER BY record_time
"""

with engine.connect() as conn:
    df = pd.read_sql(text(sql), conn)


# --- 2. 核心：特征工程 (构造 Lag Features) ---
# 逻辑：用 "T-1时刻" 和 "T-2时刻" 的水压，来预测 "T时刻" 的水压
print("正在构造特征...")

# 提取时间特征 (你原本的计划)
df['hour'] = df['record_time'].dt.hour
df['dayofweek'] = df['record_time'].dt.dayofweek

# 查看扩容后的df，扩容后的df添加了hour和dayofweek两列
print(df.head())

# 提取滞后特征 (修正后的关键计划)
# shift(1) 代表把数据往下平移1行，也就是获取"上一条数据"的值
df['pressure_lag_1'] = df['pressure'].shift(1) # 上一时刻的水压
df['pressure_lag_2'] = df['pressure'].shift(2) # 上上时刻的水压

# 查看扩容后的df，扩容后的df添加了hour、dayofweek、pressure_lag_1和pressure_lag_2四列
# 同时还能发现前两行在最后两列有空值
print(df.head())

# 因为平移会产生空值 (前2行没有"前2行")，所以要去掉
df.dropna(inplace=True)

# 查看去除空值后的df
print(df.head())

# --- 3. 划分数据集 ---
# 目标(y): 真实的水压
# 特征(X): 小时、星期、上一时刻水压、上上时刻水压
features = ['hour', 'dayofweek', 'pressure_lag_1', 'pressure_lag_2']
target = 'pressure'

X = df[features]
y = df[target]

# 必须要按时间顺序切分，不能随机打乱！(shuffle=False)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)

# --- 4. 模型训练与调参 ---
print("开始训练 XGBoost...")
xgb = XGBRegressor(objective='reg:squarederror')

# 简单的网格搜索
param_grid = {
    'n_estimators': [50, 100],     # 树的数量
    'learning_rate': [0.05, 0.2],  # 学习率
    'max_depth': [3, 5]            # 树的深度
}

grid_search = GridSearchCV(estimator=xgb, param_grid=param_grid, cv=3, scoring='neg_mean_absolute_error')

# 开始模型训练
grid_search.fit(X_train, y_train)

best_model = grid_search.best_estimator_
print(f"最优参数: {grid_search.best_params_}")

# --- 5. 评估 (修正指标) ---
preds = best_model.predict(X_test)
mae = mean_absolute_error(y_test, preds)
rmse = np.sqrt(mean_squared_error(y_test, preds))

print(f"✅ 模型评估结果:")
print(f"MAE (平均绝对误差): {mae:.4f}")
print(f"RMSE (均方根误差): {rmse:.4f}")

# --- 6. 模型保存 ---
joblib.dump(best_model, 'pressure_xgb.pkl')
print("模型已保存为 pressure_xgb.pkl")
