def complex_decorator(func):

    def comefrom():
        print("我从承德来，要到")

    def destination():
        print("是我要去的地方")

    def wrapper():
        comefrom()
        func()
        destination()

    return wrapper


@complex_decorator
def myPlace():
    print("杭州")


myPlace()
