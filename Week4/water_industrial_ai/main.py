import sys
import os
import time

# 这一步很重要：把当前目录加入到 Python 的搜索路径中
# 这样 Python 才能找到 data, models, reports 这些文件夹
sys.path.append(os.getcwd())


def main():
    print("=" * 60)
    print("🌊 北水云服 AI 算法工程全流程 - 启动中")
    print("=" * 60)

    start_time = time.time()

    # --- 1. 导入模块 (懒加载模式) ---
    # 放在 try 块里，防止因为某个文件没写好导致整个程序直接崩溃
    try:
        from data import generate_data
        from models import train_pressure_xgb
        from reports import generate_report
        from utils import ts_db_loader
    except ImportError as e:
        print(f"❌ 严重错误：模块导入失败 -> {e}")
        print("💡 提示：请检查 data/models/reports 文件夹下是否有 __init__.py 文件")
        return

    # --- 2. 执行步骤 1：数据工程 ---
    print("\n📦 [Step 1] 数据生成与入库")
    print("-" * 30)
    # 调用我们刚才写好的 run() 函数
    if not generate_data.run():
        print("🛑 数据生成失败，流程终止")
        return

    # --- 3. 执行步骤 2：模型训练 ---
    print("\n🧠 [Step 2] 模型训练 (XGBoost)")
    print("-" * 30)
    if not train_pressure_xgb.run():
        print("⚠️ 模型训练遇到问题，但继续执行...")

    # --- 4. 执行步骤 3：自动化报表 ---
    print("\n📊 [Step 3] 生成周报")
    print("-" * 30)
    generate_report.run()

    # --- 5. 执行步骤 4 (可选)：时序数据库加载 ---
    print("\n⏱️ [Step 4] InfluxDB 时序数据写入")
    print("-" * 30)
    # utils 里的文件如果没封装 run()，这里直接调用可能会报错
    # 如果你也想跑这个，记得去 utils/ts_db_loader.py 里也包一个 run()
    # 这里暂时注释掉，避免报错
    # ts_db_loader.run()
    print("   (此步骤暂略，需封装 ts_db_loader.py 后开启)")

    # --- 结束 ---
    end_time = time.time()
    duration = end_time - start_time
    print("\n" + "=" * 60)
    print(f"✅ 全流程执行完毕！总耗时: {duration:.2f} 秒")
    print("=" * 60)


if __name__ == "__main__":
    main()
