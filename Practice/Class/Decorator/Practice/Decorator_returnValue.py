# 如果原函数有 return，但装饰器里的 wrapper 忘了写 return，那么结果就会变成 None
def return_decorator(func):
    def wrapper(*args, **kwargs):
        print("🧮 正在计算...")
        # ❌ 错误写法： func(*args, **kwargs) -> 这样只是运行了，结果丢了！
        
        # ✅ 正确写法：必须用变量接住结果，最后返回
        result = func(*args, **kwargs)
        return result 
    return wrapper

@return_decorator
def add(a, b):
    return a + b

# 运行
x = add(3, 5)
print(f"结果是: {x}") # 如果没写 return，这里 x 就是 None