class MyList:
    def __init__(self, data):
        self.data = data

    def __getitem__(self, index):
        return self.data[index]

    def __len__(self):
        return len(self.data)

l = MyList([1, 2, 3])
print(l[0])   # 触发 __getitem__ -> 输出 1
print(len(l)) # 触发 __len__ -> 输出 3