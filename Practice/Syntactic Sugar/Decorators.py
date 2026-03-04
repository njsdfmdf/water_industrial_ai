def sleep():
    print("💤 我正在睡觉...")

print("------------笨办法-----------")
def sleep():
    print("🪥 刷牙")     # 新加的
    print("💤 我正在睡觉...")
    print("⏰ 定闹钟")     # 新加的


print("-------------装饰器-------------")
# 这是一个装饰器函数（相框制作机）
def add_routine(func):
    
    # 这是一个内部函数（相框本身）
    # 它负责把“旧函数”夹在中间，前后加料
    def wrapper():
        print("🪥 刷牙 (这是装饰器加的功能)")
        func()  # <--- 这里调用了原始的函数（比如 sleep）
        print("⏰ 定闹钟 (这是装饰器加的功能)")
        
    return wrapper  # 返回制作好的带相框的函数

def sleep():
    print("💤 我正在睡觉...")

# 手动包装：把 sleep 扔进去，变成一个新的函数
sleep = add_routine(sleep)

# 运行看看
sleep()

print("----------语法糖写法-----------")
@add_routine  # 只要把这一行放在函数头上
def sleep():
    print("💤 我正在睡觉...")

# 当你写了 @add_routine，Python 解释器在后台悄悄帮你做了一件事：它自动把下面的函数扔进 add_routine 里，然后把返回的新函数覆盖掉原来的名字。

print("-----------装饰器的万能模板------------")
def my_decorator(func):
    # *args 和 **kwargs 意思就是“不管你有多少参数，我都接着”
    def wrapper(*args, **kwargs):
        print("--- 🟢 运行前干坏事 ---")
        
        # 运行原函数，并把参数原封不动传进去
        result = func(*args, **kwargs)
        
        print("--- 🔴 运行后干坏事 ---")
        return result # 如果原函数有返回值，这里要记得送回去
        
    return wrapper