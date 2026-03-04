f = open('data.txt')
data = f.read()
# 如果中间报错了，这行可能执行不到，导致文件泄露
f.close()

# 语法糖写法
with open('data.txt') as f:
    data = f.read()
# 即使报错，离开缩进块后文件也会自动关闭