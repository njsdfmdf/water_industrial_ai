from abc import ABC, abstractmethod
from typing import Any

class BaseFunction(ABC):
    def __init__(self, name, age) -> None:
        self.name = name
        self.age = age
    
    @abstractmethod
    def Quality(self):
        pass

class NormalFunction(BaseFunction):
    def __init__(self, name, age, quality) -> None:
        super().__init__(name, age)

        self.quality = quality
    
    def __call__(self, numKiss) -> Any:

        self.Quality(self.quality)
        
        result_str = str(f"{self.name} 亲了薛鹏{numKiss}次")
        return result_str
    
    def Quality(self, quality):
        print(f"{self.name} 是个 {quality} 的人")
    
class PervertFunction(BaseFunction):
    def __init__(self, name, age, quality) -> None:
        super().__init__(name, age)

        self.quality = quality

    
    def __call__(self, numFuck) -> Any:
        
        self.Quality(self.quality)

        result_str = str(f"{self.name} 被薛鹏上了{numFuck}次")
        return result_str
    
    def Quality(self, quality):
        print(f"{self.name} 是个 {quality} 的人")
    
    
def run_pipeline(transformers, data):
    for tf in transformers:
        result = tf(data)
        print(result)

t1 = NormalFunction("吕劲昕", 20, "温柔")
t2 = PervertFunction("程智慧", 24, "骚")

run_pipeline([t1, t2], [10, 20])