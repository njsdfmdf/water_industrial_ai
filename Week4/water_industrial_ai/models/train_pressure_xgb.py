import pandas as pd
import numpy as np
import joblib
import os
from sqlalchemy import create_engine, text
from xgboost import XGBRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.model_selection import train_test_split, GridSearchCV

# --- 关键修改：导入我们刚才写的 db_loader ---
# 注意：由于最终是在 main.py 运行，sys.path 包含了根目录
# 所以我们可以直接从 data 包导入
from data.db_loader import load_pressure_training_data

def run():
    """模型训练入口函数"""
    try:
        
        df = load_pressure_training_data()

        if df is None or df.empty:
            print("   [Model] ❌ 无法获取训练数据，终止训练")
            return False

        # --- 划分 ---
        features = ["hour", "dayofweek", "pressure_lag_1", "pressure_lag_2"]
        target = "pressure"

        X = df[features]
        y = df[target]
        
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, shuffle=False
        )

        # --- 训练 ---
        print("   [Model] 开始训练 XGBoost...")
        xgb = XGBRegressor(objective="reg:squarederror")
        param_grid = {
            "n_estimators": [50],  # 为了演示速度，减少数量
            "learning_rate": [0.1],
            "max_depth": [3],
        }
        grid_search = GridSearchCV(
            estimator=xgb, param_grid=param_grid, cv=2
        )  # 为了速度 cv改小
        grid_search.fit(X_train, y_train)

        best_model = grid_search.best_estimator_

        # --- 评估 ---
        preds = best_model.predict(X_test)
        mae = mean_absolute_error(y_test, preds)
        print(f"   [Model] ✅ 训练完成! MAE: {mae:.4f}")

        # --- 保存 ---
        # 确保保存到 models 文件夹下，而不是根目录
        save_path = "models/pressure_xgb.pkl"
        joblib.dump(best_model, save_path)
        print(f"   [Model] 模型已保存至: {save_path}")
        return True

    except Exception as e:
        print(f"   [Model] ❌ 训练失败: {e}")
        return False


if __name__ == "__main__":
    run()
