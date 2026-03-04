class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def __str__(self):
        return f"{self.name} 是一个 {self.age} 岁的工程师"

p = Person("Mike", 25)
print(p)  # 触发 __str__ -> 输出: Mike 是一个 25 岁的工程师