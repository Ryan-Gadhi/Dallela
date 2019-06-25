import threading

z = 0
def look_for_trigger():
    for z in range(1000000):
        z = z




def sound():
    print("im in")
    while z < 9999:
        print(z)

x = threading.Thread(target=look_for_trigger)
x.start()
print(x.isAlive())