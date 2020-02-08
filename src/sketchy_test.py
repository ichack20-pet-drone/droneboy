from pyparrot.Minidrone import Mambo
from threading import Thread

drone = Mambo("d0:3a:86:9d:e6:5a")

def tryme():
    drone.connect(5)
    drone.smart_sleep(3)
    
    drone.safe_takeoff(5)
    drone.smart_sleep(3)
    
    drone.safe_land(5)
    drone.smart_sleep(3)

    drone.disconnect()

print("normal")
tryme()
print("normal done")

# print("thread stuff")
# t = Thread(target=tryme)
# t.start()
# t.join()
# print("thread stuff done")

print("done done")