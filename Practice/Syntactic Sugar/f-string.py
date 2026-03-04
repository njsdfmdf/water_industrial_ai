name = "Alice"
age = 25
print("我是 " + name + "，今年 " + str(age) + " 岁。")
# 或者
print("我是 {}，今年 {} 岁。".format(name, age))

# 语法糖写法
print(f"我是 {name}，今年 {age} 岁。")