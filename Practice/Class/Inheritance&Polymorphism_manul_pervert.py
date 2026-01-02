from abc import ABC, abstractclassmethod
from typing import Any

class BaseFunction:
    def __init__(self, name, age) -> None:
        self.name = name
        self.age = age
    
    @abstractclassmethod
    def Quality(self):
        pass

class NormalFunction(BaseFunction):
    def __init__(self, name, age, quality) -> None:
        super().__init__(name, age)

        self.quality = quality
    
    def __call__(self, numKiss) -> Any:
        print(f"{self.name} 是个 {self.quality} 的人")
        result_str = str(f"{self.name} 亲了薛鹏{numKiss}次")
        return result_str
    
class PervertFunction(BaseFunction):
    def __init__(self, name, age, quality) -> None:
        super().__init__(name, age)

        self.quality = quality
        
    
    def __call__(self, numFuck) -> Any:
        print(f"{self.name} 是个 {self.quality} 的人")
        result_str = str(f"{self.name} 被薛鹏上了{numFuck}次")
        return result_str
    
def run_pipeline(transformers, data):
    for tf in transformers:
        result = tf(data)
        print(result)

t1 = NormalFunction("吕劲昕", 20, "温柔")
t2 = PervertFunction("程智慧", 24, "骚")

run_pipeline([t1, t2], [10, 20])