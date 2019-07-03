



class A(object):
    def __new__(cls):
        print("A.__new__ called")
        return super(A, cls).__new__(cls)

    def __init__(self):
        print("A.__init__ called")

class B(A):

    def speak(self):
        print('B is speaking')


class B_son(B):

    def speak(self):
        print('B_son is speaking')


# B_son()
# B()
# print('finished')

import threading
import time


class Singleton(object):

    def __new__(cls, *args, **kw):
        if not hasattr(cls, '_instance'):
            cls._instance = super(Singleton, cls).__new__(cls, *args, **kw)

            print('\n')
            print('cls is ', cls)
            print(type(cls._instance),  cls._instance)

        else:
            print(' {}  already exists'.format(cls._instance))
        return cls._instance


class Bus(Singleton):
    def sendData(self,data):
        pass


class BusSon(Bus):
    def sendData(self,data):
        pass


if __name__ == '__main__':


    busson1 = BusSon()
    bus1 = Bus()
    print('------------------------\n')

    busson2 = BusSon()
    bus2 = Bus()

    print('------------------------\n')


    Bus.__new__(BusSon)
    Bus()
    x = Singleton.__new__(Bus)
    print(x)
