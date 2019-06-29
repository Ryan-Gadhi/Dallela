from speaking import Speaking
import threading
sp = None

def fun1():
	global sp
	sp = Speaking()
	sp.say('testing 1')
	sp.say('testing 2')

def fun2():
	sp.say('testing 3')


