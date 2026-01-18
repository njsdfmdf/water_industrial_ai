import joblib
import json

# 1. 加载模型
try:
    best_model = joblib.load('pressure_xgb.pkl')
    print("✅ 模型加载成功！")
except FileNotFoundError:
    print("❌ 找不到模型文件，请确认文件名和路径是否正确。")
    exit() # 没文件就别往下跑了


# 1. 获取所有参数（此时包含很多 None）
all_params = best_model.get_params()

# 2. 过滤：只保留那些值不是 None 的参数
useful_params = {k: v for k, v in all_params.items() if v is not None}

# 3. 漂亮地打印出来
import pprint # 这是一个让打印更漂亮的内置库
pprint.pprint(useful_params)


# 2. 获取底层配置
try:
    config_str = best_model.get_booster().save_config()
    config = json.loads(config_str)

    # --- 修改点开始 ---
    
    # 策略 A：先看最外层有哪些大类（通常会有 learner, version 等）
    print("--- 顶层结构 ---")
    print(config.keys()) 

    # 策略 B：查看 learner 这一层的所有配置（推荐）
    # 这里面通常包含了主要的训练参数
    print("\n--- Learner 参数详解 ---")
    if 'learner' in config:
        # 只打印 learner 下的第一层键值，防止刷屏
        # 如果你想看全部，直接 print(json.dumps(config['learner'], indent=4))
        print(json.dumps(config['learner'], indent=4))
    else:
        print("⚠️ 奇怪，配置里居然没有 'learner' 字段？")

    # --- 修改点结束 ---

except Exception as e:
    print(f"❌ 查看配置时出错: {e}")