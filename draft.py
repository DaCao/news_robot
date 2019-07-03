from time import sleep
import signal
import time
from multiprocessing import Process
from os import getpid


def child_process():
    # child process
    # 忽略 child process 的 SIGHUP 信号
    signal.signal(signal.SIGHUP, signal.SIG_IGN)
    print("child process's pid: %d" % getpid())
    while (1):
        print("child's still alive.")
        time.sleep(1)


def main():
    p = Process(target=child_process)
    """
    这里就不能再设置 daemon 属性为 True 了，
    因为如果 daemon 属性为 True，则 Process 进程结束时会自动 terminate 所有的子进程
    这样就没 SIGHUP 什么事了
    """
    p.start()
    # parent process
    print("Parent process ends here.")
    print("Will child process live forever?")


if __name__ == '__main__':
    main()



'''

def child_process():
    # 子进程函数
    # 建立一个进程，每隔一秒钟输出"child's still alive."
    while (1):
        print("child's still alive.")
        sleep(1)


def main():
    # 主进程函数
    p = Process(target=child_process)
    p.daemon = True  # 设置 daemon 属性为 True
    p.start()
    sleep(10)  # 休眠 10 秒后结束
    print("Main process ends.")
    print("Will child process live forever?")  # 我们期待子进程继续活着，但事实上……


if __name__ == "__main__":
    main()
'''