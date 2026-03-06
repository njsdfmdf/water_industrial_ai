from abc import ABC, abstractmethod
from typing import Any

# 在普通的面向对象中，你可以直接拿父类造一个对象出来。但是，一旦父类继承了 ABC，并且里面有抽象方法，它就变成了一张纯粹的图纸（概念），而不是一个实物。
# ABC 单独出现威力还没那么大，它最经典的搭档就是你代码里的 @abstractmethod（抽象方法装饰器）。
# 这句话的意思是：“作为包工头，我在这里定下了一个死规矩：只要是我的子类，不管你是谁，你都必须自己写一个叫 Quality 的函数！”

class BaseFunction(ABC):
    def __init__(self, name, age):
        self.name = name
        self.age = age

    @abstractmethod
    def Quality(self):
        pass


class NormalFunction(BaseFunction):
    def __init__(self, name, age, quality):

        # 因为父类里写了def.__init__(self, name, age)，所以子类中的__init__()就必须写出name和age
        super().__init__(name, age)
        # 因为super().__init__()中显示的写出了name和age，所以在子类的方法中就不需要写出
        # self.name = name
        # self.age = age

        self.quality = quality

    def __call__(self, numKiss):
        # 写self的意义在于让python知道这个方法时内部方法
        self.Quality(self.age)

        result_str = str(f"{self.name} 亲了薛鹏{numKiss}次")
        return result_str

    def Quality(self, age):
        print(f"她{age}岁了")
        print(f"{self.name} 是个 {self.quality} 的人")


class PervertFunction(BaseFunction):
    def __init__(self, name, age, quality):
        super().__init__(name, age)

        self.quality = quality

    def __call__(self, numFuck):

        self.Quality()

        result_str = str(f"{self.name} 被薛鹏上了{numFuck}次")
        return result_str

    def Quality(self):
        print(f"{self.name} 是个 {self.quality} 的人")


def run_pipeline(transformers, data):
    for tf in transformers:
        result = tf(data)
        print(result)


t1 = NormalFunction("吕劲昕", 28, "温柔")
t2 = PervertFunction("程智慧", 24, "骚")

run_pipeline([t1, t2], 10)
