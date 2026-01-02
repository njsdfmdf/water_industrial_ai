# 1.定义装饰器
def simple_decorator(func):
    def wrapper():
        print("我来到了")
        func()
        print("是我来到的地方")
    return wrapper

# 2.使用装饰器
@simple_decorator
def myPlace(): # 运行到此行代码时myPlace只是一个名字了，名字背后的函数是wrapper()
    print("西安")

# 3.运行
myPlace() # 此时运行的其实是wrapper()