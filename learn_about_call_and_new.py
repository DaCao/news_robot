#
# class Meta_1(type):
#     def __call__(cls, *a, **kw):
#         print("entering Meta_1.__call__()")
#
#
#         print(cls.mro())
#         print('         ', cls)
#         print('         ', super(Meta_1, cls).__self__)
#
#
#         rv = super(Meta_1, cls).__call__(*a, **kw)
#         print("exiting Meta_1.__call__()")
#         return rv
#
#
# class Car(object, metaclass=Meta_1):
#
#     def __new__(cls, *a, **kw):
#         print("entering Car.__new__()")
#         print(super(Car, cls).__self__)
#         rv = super(Car, cls).__new__(cls, *a, **kw)
#         print("exiting Car.__new__()")
#         return rv
#
#     def __init__(self, *a, **kw):
#         print("executing Car.__init__()")
#         super(Car,self).__init__(*a, **kw)
#
# if __name__ == '__main__':
#
#     c = Car()



class Meta_1(type):
    def __call__(cls, *a, **kw):
        print('\n\n')
        print("entering Meta_1.__call__()")

        print(cls.mro())
        print(cls)
        print(super(Meta_1, cls).__self__)

        # print(super(cls, Dummy).__self__)

        super(Meta_1, cls).__call__(*a, **kw)


        rv = super(Meta_1, cls).__call__(*a, **kw)
        print("exiting Meta_1.__call__()")
        return rv


class DummyO(object):
    pass


class Dummy(object, metaclass=Meta_1):
    pass


class Car(object, metaclass=Meta_1):

    def __new__(cls, *a, **kw):
        print("Car.__new__()")
        rv = super(Car, cls).__new__(cls, *a, **kw)
        return rv

    def __init__(self, *a, **kw):
        print("Car.__init__()")
        print(super(Car,self).__self__)
        super(Car,self).__init__(*a, **kw)

if __name__ == '__main__':

    print(type(DummyO), type(object))
    print(type(Meta_1))
    print(type(Car))
    print(Meta_1.mro(Meta_1))
    print(type(Meta_1).mro(Meta_1))
    print(Car.mro())
    print(type(Car).mro(Car))
    exit()



    c = Car()   # __call__ is an instance method; Car is an instance of Meta_1;
                # Car() is equivalent to Meta_1.__call__(Car)
                # Car() is really short for Meta_1.__call__(Car)
