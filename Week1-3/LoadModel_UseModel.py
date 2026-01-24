import joblib
import pandas as pd

# 加载模型
loaded_model = joblib.load("pressure_xgb.pkl")

# 加载数据
df_new = pd.read_csv("future_data.csv")

# 提取特征 (确保只把模型认识的列喂给它)
feature_cols = ["hour", "dayofweek", "pressure_lag_1", "pressure_lag_2"]
X_new = df_new[feature_cols]

# 使用模型
preds = loaded_model.predict(X_new)
