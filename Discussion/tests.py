from tkinter import *

import threading


def look_for_trigger():

    for i in range(10000):
        x = i
    return "dfhdfshsdfh"


def sound():
    print(look_for_trigger())


root = Tk()

var = StringVar()

var.set('hello')

l = Label(root, textvariable=var)

l.pack()

t = Entry(root, textvariable=var)

t.pack()

x = threading.Thread(target=sound)
y = x.start()
print()

root.mainloop()  #
