import logging
import threading
import time

def thread_function():
    while(1):
        print ('hellow thread')

def thread_function2(name):
    while(1):
        print ('hellow thread2')


if __name__ == "__main__":
    x = threading.Thread(target=thread_function)
    y = threading.Thread(target=thread_function2, args=(1,))
    x.start()
    y.start()
