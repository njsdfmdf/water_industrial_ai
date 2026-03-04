import time

def timer(func):
    """
    这是一个用来计算函数运行时间的装饰器
    """
    def wrapper(*args, **kwargs):
        # 🟢 1. 记录开始时间
        start_time = time.time()
        
        # 🟡 2. 真正执行函数 (并接住它的返回值)
        result = func(*args, **kwargs)
        
        # 🔴 3. 记录结束时间
        end_time = time.time()
        
        # 🔵 4. 计算并打印耗时
        duration = end_time - start_time
        print(f"⏱️ 函数 [{func.__name__}] 运行耗时: {duration:.4f} 秒")
        
        # ⚫ 5. 把原函数的返回值送回去 (千万别忘了这一步！)
        return result
        
    return wrapper

# 使用装饰器
@timer
def heavy_work():
    print("开始做繁重的工作...")
    time.sleep(2)  # 假装让程序睡2秒，模拟耗时操作
    print("工作完成！")

@timer
def add(a, b):
    time.sleep(0.5) # 假装算得很慢
    return a + b

# --- 开始测试 ---

# 测试 1: 没有返回值的函数
heavy_work()
print("-" * 20)

# 测试 2: 有参数且有返回值的函数
sum_result = add(10, 20)
print(f"计算结果是: {sum_result}")