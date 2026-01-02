# class Pump:
#     def __init__(self, name) -> None:
#         self.name = name

#     def introduce(self):
#         print(f"I am a pump: {self.name}")

# pump = Pump("Pump A")
# pump.introduce()

class WaterTank:
    def __init__(self, level):
        self.current_level = level  # <--- 错误1: 应该存进 self 吗？
    
    def add_water(self, amount):     # <--- 错误2: 参数少了什么？
        self.current_level += amount # <--- 错误3: 能直接访问 current_level 吗？
        print(f"加水成功，当前水位: {self.current_level}")

# 测试
tank = WaterTank(10)
tank.add_water(5)