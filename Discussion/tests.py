import logging
import threading
import time


number = 0


def changeValue():
    while(1):
        global number
        number +=1

def printing():
    while(1):
        print(number)

t1 = threading.Thread(target=changeValue)
t2 = threading.Thread(target=printing)

for i in range(3):
    t1.start()
    t2.start()


