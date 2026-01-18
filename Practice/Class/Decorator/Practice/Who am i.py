# 防止原函数的身份信息丢失
import functools


def identity_decorator(func):
    @functools.wraps(
        func
    )  # 👈 这就是“伪装术”，让 wrapper 看起来像原函数，将my_function的身份信息粘贴到wrapper的身上
    def wrapper(*args, **kwargs):
        print("调试中...")
        return func(*args, **kwargs)

    return wrapper


@identity_decorator
def my_function():
    """这是我的函数文档"""  # 这种写法叫：说明书。必须写在函数（或类/模块的第一行）
    pass


# __name__用来输出函数的真实名字
print(my_function.__name__)  # 输出: my_function (如果没加那行，会输出 wrapper)
print(my_function.__doc__)  # 输出: 这是我的函数文档
