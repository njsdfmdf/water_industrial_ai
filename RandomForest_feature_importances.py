import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
import matplotlib.pyplot as plt
import pandas as pd
from sqlalchemy import create_engine, text

from sklearn.model_selection import train_test_split

engine = create_engine("mysql+pymysql://root:123456@localhost:3306/water_db")

sql = f"""
    SELECT * FROM device_maintenance
"""

with engine.connect() as conn:
        df = pd.read_sql(text(sql), conn)

    
print(f"原始数据量: {len(df)}")

# 选特征 (去掉无用的 ID 类字段)
features = ['air_temp', 'process_temp', 'rot_speed', 'torque', 'tool_wear']
X = df[features]
y = df['target'] # 预测是否故障

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 训练
rf = RandomForestClassifier(n_estimators=100)
rf.fit(X_train, y_train)

# --- 重点：特征重要性可视化 ---
importances = rf.feature_importances_
indices = np.argsort(importances)[::-1] # 降序排列

plt.figure(figsize=(10, 6))
plt.title("Key Factors for Device Failure (Feature Importance)")
plt.bar(range(X.shape[1]), importances[indices], align="center")
plt.xticks(range(X.shape[1]), [features[i] for i in indices])
plt.tight_layout()
plt.savefig('feature_importance.png') # 保存图片
print("特征重要性图表已保存！")

# --- 评估 ---
y_pred = rf.predict(X_test)
print(classification_report(y_test, y_pred)) # 这里面包含了 准确率、召回率、F1