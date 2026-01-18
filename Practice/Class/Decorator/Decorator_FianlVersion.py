import functools
import datetime


# 定义装饰器
def industrial_logger(func):
    """
    一个用于打印详细执行日志的装饰器
    """

    @functools.wraps(func)  # 保持原函数的元数据
    def wrapper(*args, **kwargs):
        # 1. 执行前逻辑
        start_time = datetime.datetime.now()
        print(f"⏰ [{start_time.strftime('%H:%M:%S')}] 开始执行任务: {func.__name__}")

        try:
            # 2. 执行原函数
            result = func(*args, **kwargs)

            # 3. 执行后逻辑
            print(f"✅ 任务 {func.__name__} 成功完成。")
            return result

        except Exception as e:
            # 4. 异常捕获逻辑
            print(f"❌ 警告: {func.__name__} 执行失败! 错误: {e}")
            raise e  # 继续抛出异常，不要吞掉

    return wrapper


# --- 使用装饰器 ---


@industrial_logger
def process_water_data(rows):
    print(f"⚙️ 正在处理 {rows} 行数据...")
    if rows < 0:
        raise ValueError("行数不能为负数")
    return rows * 2


# 测试正常情况
process_water_data(100)

# 测试异常情况 (观察装饰器如何捕获日志)
try:
    process_water_data(-5)
except:
    pass
