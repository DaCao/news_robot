#encoding=utf8
# https://yq.aliyun.com/articles/70418

import threading
import time


#这里使用方法__new__来实现单例模式
class Singleton(object):#抽象单例

    def __new__(cls, *args, **kw):
        if not hasattr(cls, '_instance'):
            orig = super(Singleton, cls)
            cls._instance = orig.__new__(cls, *args, **kw)

            print('\n----------------------')
            # print('cls is ', cls)
            # print(type(cls._instance),  cls._instance)
            print(Singleton, '     cls is ', cls, '      super(Singleton, cls) is ', orig)
            # print(type(cls._instance), id(cls._instance), cls._instance)
        else:
            print(' {}  already exists'.format(cls._instance))
        return cls._instance


#总线
class Bus(Singleton):
    lock = threading.RLock()
    def sendData(self,data):

        print('{} {} trying to acquire lock...'.format(type(self), id(self)))
        self.lock.acquire()
        print('\n {} {} lock acquired! \n'.format(type(self), id(self)))
        time.sleep(3)
        print("{} {} Sending Signal Data...".format(type(self), id(self)),data)
        self.lock.release()



class BusSon(Bus):
    lock = threading.RLock()
    def sendData(self,data):

        print('{} {} trying to acquire lock...'.format(type(self), id(self)))
        self.lock.acquire()
        print('\n {} {} lock acquired! \n'.format(type(self), id(self)))
        time.sleep(3)
        print("{} {} Sending Signal Data...".format(type(self), id(self)),data)
        self.lock.release()



#线程对象，为更加说明单例的含义，这里将Bus对象实例化写在了run里
class VisitEntity(threading.Thread):

    my_bus=""
    name=""

    def getName(self):
        return self.name
    def setName(self, name):
        self.name=name
    def run(self):
        self.my_bus=Bus()
        print('\n ----- VisitEntity {} is running \n'.format(id(self)))
        self.my_bus.sendData(self.name)



if  __name__=="__main__":

    # for i in range(3):
    #     print("Entity %d begin to run..."%i)
    #     my_entity=VisitEntity()
    #     my_entity.setName("Entity_"+str(i))
    #     my_entity.start()



    # busson = BusSon()
    # busson2 = BusSon()
    print('------------------------\n')

    # bus1 = Bus()
    # bus2 = Bus()

    print('------------------------\n')

    # s = Singleton()
    # print('  ')
    # print(s)
    # print(' ')

    Bus.__new__(BusSon)
    Bus()
    x = Singleton.__new__(Bus)
    print(x)
