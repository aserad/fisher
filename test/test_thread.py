# -*- encoding: utf-8 -*-

from werkzeug.local import Local
import threading
import time


class A:
    b = 1


my_obj = Local()
my_obj.b = 1


def worker():
    my_obj.b = 2
    print(f'in new thread b is: {my_obj.b}')


new_t = threading.Thread(target=worker, name='haha_thread')
new_t.start()

time.sleep(1)
print(f'in main thread b is: {my_obj.b}')
