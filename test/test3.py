# -*- encoding: utf-8 -*-

import threading
from werkzeug.local import LocalStack
import time

my_stack = LocalStack()
my_stack.push(1)
print(f'in main thread after push, value is: {my_stack.top}')


def worker():
    print(f'...in new thread before push, value is: {my_stack.top}')
    my_stack.push(2)
    print(f'...in new thread after push, value is: {my_stack.top}')


t = threading.Thread(target=worker)
t.start()

time.sleep(2)
print(f'finally, in main thread, value is: {my_stack.top}')

