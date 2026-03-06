def black_hole(*args, **kwargs):
    print(f"编织袋里装了无名参数: {args}")
    print(f"收纳盒里装了带名参数: {kwargs}")

# 随便怎么传都不会报错！
black_hole(1, 2, 3) 
# 输出: 编织袋里装了无名参数: (1, 2, 3) / 收纳盒里装了带名参数: {}

black_hole(name="薛鹏", age=25) 
# 输出: 编织袋里装了无名参数: () / 收纳盒里装了带名参数: {'name': '薛鹏', 'age': 25}

black_hole("苹果", "香蕉", price=10, color="red")
# 输出: 编织袋里装了无名参数: ('苹果', '香蕉') / 收纳盒里装了带名参数: {'price': 10, 'color': 'red'}

# *args (Arguments)：就像是一个大号编织袋。只要是没有贴名字标签的东西（比如 10, "张三", True），你都可以往里面扔。Python 会自动把它们打包成一个元组 (Tuple)。

# **kwargs (Keyword Arguments)：就像是一个带格子的收纳盒。只要是贴了名字标签的东西（比如 age=20, name="李四"），你都可以塞进去。Python 会自动把它们打包成一个字典 (Dictionary)。

# 注： 这里的 args 和 kwargs 只是程序员约定的习惯缩写（你叫 *a 和 **b 也行，但通常不这么干），真正起魔法作用的是前面的星号 * 和 **。