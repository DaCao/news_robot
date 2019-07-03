


# https://stackoverflow.com/questions/6760685/creating-a-singleton-in-python
# method 2  vs  method 3



class Singleton1(object):
    _instance = None

    def __new__(cls, *args):
        if not isinstance(cls._instance, cls):
            cls._instance = super(Singleton1, cls).__new__(cls, *args)
        return cls._instance


class Singleton2(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton2, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

    def get_instance(cls):
        return cls._instances[cls]

class Base(object):

    def __init__(self):
        pass

if __name__ == '__main__':

    class MyClass1(Singleton1):
        def __init__(self):
            pass

    class MyClass2(Base, metaclass=Singleton2):
        def __init__(self):
            pass


    x1 = MyClass1()
    x2 = MyClass2()

    print(MyClass1.__class__)
    print(MyClass2.__class__)