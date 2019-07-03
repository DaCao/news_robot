import os
from abc import ABCMeta
import abc


class CommonInterFace():
    __metaclass__ = ABCMeta

    @abc.abstractmethod
    def action_1(self):
        pass


class RealObject(CommonInterFace):

    def __init__(self, *args, **kwargs):
        self.data = kwargs['data']

    def action_1(self):
        return "doing A heavy computation"


class ObjectProxy(CommonInterFace):
    __cache = None

    def __init__(self, *args, **kwargs):
        if not self.__class__.__cache:
            self.__class__.__cache = RealObject(*args, **kwargs)
            print("Object Created")
        else:
            self.__class__.__cache.data = kwargs['data']
            print("Using cached Object")

    def action_1(self):
        return self.__class__.__cache.action_1()


if __name__ == '__main__':
    dump = range(1, 100)
    data = range(0, 100)
    for i in data:
        inst = ObjectProxy(data=dump)
        print(inst.action_1())
