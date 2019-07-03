



class A(object):

    name = 'da'
    address = 'hell'
    tel = '608'
    count = 0

    # def __new__(cls):
    #     print("A.__new__ called")
    #     # print(cls, id(cls), type(cls))
    #     # print(A, id(A), type(A))
    #     shit = super(A, cls).__new__(cls)
    #     # print(shit)
    #     return shit

    def __init__(self):
        # print("A.__init__ called")
        # print(self.__class__, id(self.__class__))
        print(self.name, id(self.name))
        # self.count += 1
        # print(self.count)




a1 = A()
a1.name = 'fuck you'
a2 = A()
a2.name = 'fuck you'
a3 = A()
a3.name = 'fuck you'
a3.name = 'caonima'

print(a1.name, a2.name, a3.name)
print(id(a1.name), id(a2.name), id(a3.name))
print(id(a1), id(a2), id(a3))

print(A.mro())


'''
da 4328000344
fuck you
da 4328000344
da 4328000344
fuck you da da
4328038256 4328000344 4328000344
4367385824 4367385936 4367385992
'''