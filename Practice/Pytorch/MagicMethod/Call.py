class Multiplier:
    def __call__(self, x):
        return x * 10

m = Multiplier()
print(m(5)) # 触发 __call__ -> 像函数一样调用对象 -> 输出 50