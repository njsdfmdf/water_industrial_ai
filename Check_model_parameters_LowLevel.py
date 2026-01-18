import joblib

# 1. 尝试加载（解冻）
# 只要这行不报错，说明保存成功了！
loaded_model = joblib.load('pressure_xgb.pkl')

print("✅ 模型加载成功！它现在复活了。")
print(loaded_model) # 打印看看它的参数

