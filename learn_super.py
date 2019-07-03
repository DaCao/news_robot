# coding=utf-8


from functools import partial

# class Super:
#     def __init__(self, sub_cls, instance):
#         # 假设 sub_cls = B, instance = D()
#         # Super(B, self).add(233)
#         mro = instance.__class__.mro()
#         # mro == [D, B, C, A, object]
#         # sub_cls is B
#         # 从 mro 中 sub_cls 后面的类中进行查找
#         # __mro_tail == [C, A, object]
#         self.__mro_tail = mro[mro.index(sub_cls)+1:]
#         self.__sub_cls = sub_cls
#         self.__instance = instance
#
#     def __getattr__(self, name):
#         # 从 mro tail 列表的各个类中查找方法
#         for cls in self.__mro_tail:
#             if not hasattr(cls, name):
#                 continue
#
#             print('call {}.{}'.format(cls, name))
#             # 获取类中定义的方法
#             attr = getattr(cls, name)
#             # 因为 d = D(); d.add(233)  等价于 D.add(d, 233)
#             # 所以返回的函数需要自动填充第一个 self 参数
#             return partial(attr, self.__instance)
#
#         raise AttributeError(name)
#



class A:
    def __init__(self):
        self.n = 2

    def add(self, m):
        print('\n\nself is {0} @A.add'.format(self))
        self.n += m


class B(A):
    def __init__(self):
        self.n = 3

    def add(self, m):
        print('\n\nself is {0} @B.add'.format(self))
        super(B, self).add(m)
        self.n += 3


class C(A):
    def __init__(self):
        self.n = 4

    def add(self, m):
        print('\n\nself is {0} @C.add'.format(self))
        super(C, self).add(m)
        self.n += 4


class D(B, C):
    def __init__(self):
        self.n = 5

    def add(self, m):
        print('\n\nself is {0} @D.add'.format(self))
        print(super(D, self).__self__)
        super(D, self).add(m)
        self.n += 5



print(D.mro())


d = D()
print(d, type(D))
d.add(2)  #D.add(d, 2)

print(d.n)







############################################################



class Base(object):
    def __init__(self):
        print("enter Base")
        print("leave Base")

# class A(Base):
#     def __init__(self):
#         print("enter A")
#         Super(A, self).__init__()
#         print("leave A")
#
# class B(Base):
#     def __init__(self):
#         print("enter B")
#         Super(B, self).__init__()
#         print("leave B")
#
# class C(A, B):
#     def __init__(self):
#         print("enter C")
#         Super(C, self).__init__()
#         print("leave C")
#
#
# class D(C):
#     def __init__(self):
#         print("enter D")
#         Super(C, self).__init__()
#         print("leave D")
#
#
# d = D()
# # c = C()
#
# print(D.mro())