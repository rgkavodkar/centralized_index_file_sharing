__author__ = 'rg.kavodkar'

import threading
import time


def print_me(text):
    time.sleep(3)
    while 1:
        print(text)


th_1 = "thread_1"
th_2 = "thread_2"
t1 = threading.Thread(target=print_me, args=(th_1,))
t2 = threading.Thread(target=print_me, args=(th_2,))
t1.start()
t2.start()

print("Main thread exit. Mic drop!")
#
# import threading
# import time
#
#
# def worker():
#     print(threading.currentThread().getName(), 'Starting')
#     time.sleep(2)
#     print(threading.currentThread().getName(), 'Exiting')
#
#
# def my_service():
#     print(threading.currentThread().getName(), 'Starting')
#     time.sleep(3)
#     print( threading.currentThread().getName(), 'Exiting')
#
# t = threading.Thread(name='my_service', target=my_service)
# w = threading.Thread(name='worker', target=worker)
# w2 = threading.Thread(target=worker) # use default name
#
# w.start()
# w2.start()
# t.start()
