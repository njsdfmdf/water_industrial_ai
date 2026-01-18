def args_decorator(func):
    # 坑点修复：wrapper 必须能接收任意参数
    def wrapper(*args, **kwargs):
        # 1.*args：专门接收没有名字的位置参数，即没有写 xx==yy这类的参数，在此例子中就是接收target，“靶子”。args的本质是一个元组args=（‘靶子’，）
        # 2.**kwargs：专门接收有名字的关键字参数，即指明了xx=yy的参数，在此例中就是bullet_type=7.62mm. 它的本质是一个字典kwargs = {'bullet_type': '7.62mm'}
        print(f"👀 [装饰器] 看到你输入了参数: {args}&{kwargs}")
        func(
            *args, **kwargs
        )  # 把参数原封不动地传给原函数，这里的args和kwargs是为了将外面传来的打包好的参数进行解包

    return wrapper


@args_decorator
def shoot(target, bullet_type="5.56mm"):
    print(f"🔫 向 {target} 发射 {bullet_type} 子弹！")


# 运行
shoot("靶子", bullet_type="7.62mm")
