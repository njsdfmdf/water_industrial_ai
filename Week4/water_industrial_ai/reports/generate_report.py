import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sqlalchemy import create_engine, text
import matplotlib.font_manager as fm
import os


def run():
    try:
        print("   [Report] 初始化绘图环境...")
        # 字体路径处理：这里假设我们是从项目根目录运行 main.py
        font_path = "fonts/simhei.ttf"

        if os.path.exists(font_path):
            my_font = fm.FontProperties(fname=font_path)
            plt.rcParams["font.family"] = my_font.get_name()
        else:
            print(f"   [Report] ⚠️ 警告：未找到字体文件 {font_path}，中文可能乱码")

        # 连接数据库
        engine = create_engine("mysql+pymysql://root:123456@localhost:3306/water_db")
        sql = "SELECT * FROM water_pressure WHERE record_time > '2023-01-01'"

        with engine.connect() as conn:
            df = pd.read_sql(text(sql), conn)

        if df.empty:
            print("   [Report] 无数据，跳过报表生成")
            return

        # 绘图逻辑
        avg_pressure = df["pressure"].mean()
        fig = plt.figure(figsize=(12, 10))
        # 如果没有中文字体，下面的中文会显示方框，但不影响程序运行
        plt.suptitle(f"本周水务运行报表\n(均值: {avg_pressure:.2f} MPa)", fontsize=16)

        ax1 = plt.subplot(2, 1, 1)
        sns.lineplot(data=df, x="record_time", y="pressure", ax=ax1, color="blue")
        ax1.set_title("水压趋势")

        ax2 = plt.subplot(2, 2, 3)
        sns.histplot(df["pressure"], bins=20, kde=True, ax=ax2, color="green")
        ax2.set_title("分布直方图")

        ax3 = plt.subplot(2, 2, 4)
        sns.boxplot(data=df, x="area", y="pressure", ax=ax3)
        ax3.set_title("区域波动")

        plt.tight_layout()

        # 确保 reports 文件夹存在
        os.makedirs("reports", exist_ok=True)
        save_path = "reports/weekly_report.png"
        plt.savefig(save_path, dpi=300)
        print(f"   [Report] ✅ 报表已生成: {save_path}")
        return True

    except Exception as e:
        print(f"   [Report] ❌ 失败: {e}")
        return False


if __name__ == "__main__":
    run()
