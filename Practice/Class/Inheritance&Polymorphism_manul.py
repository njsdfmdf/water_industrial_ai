from abc import ABC, abstractclassmethod
from typing import Any

class BaseMachine(ABC): # ABC是抽象基类模型，用于之后写@abstractclassmethod
    def __init__(self, name) -> None:
        self.name = name

    @abstractclassmethod # 在子类中必须实现work()这个方法
    def work(self):
        pass

class WaterPump(BaseMachine): # 子类WaterPump继承了父类BaseMachine

    # 这种是中规中矩的写法，需要显式的写出所有父类的基本属性，不适合父类中存在大量的基本属性的情况
    # def __init__(self, machine_id, power) -> None:

    # 使用**kwargs可以替代所有的父类中的基本属性，但是要注意需要将**kwargs写在最后的位置不然会报错

    def __init__(self, power, **kwargs) -> None:

        # 显式的指明继承父类中的那些基本属性
        # super().__init__(machine_id) 

        # 使用**kwargs可以一次性使用所有父类的属性
        super().__init__(**kwargs) 

        self.power = power
        # print(f"{self.power}KW")

    def work(self, test_data): # 子类中必须实现父类中的work()方法
        print(f"{self.name} 正在以{self.power}kw 运行，这个只是一个测试数据：{test_data}")

    def __call__(self, test_data2) -> Any: # 使用魔术方法，可以写pump()来直接调用__call__中的功能
        print(f"这是第二个测试数据：{test_data2}")


        

try:
    pump = WaterPump(machine_id="PUMP-001", power=500)
    pump.work("Sonia") # 在显示父类中的基本属性的基础上还要显示子类其他方法中的信息
    pump("Luis")
except TypeError as e:
    print(f"错误：{e}")

