from queue import Queue
from pyparrot.Minidrone import Mambo
from threading import Thread


class DroneController():
    def __init__(self, mac_address, debug=False):
        self.flying = False
        self.commands = Queue()
        self.drone = Mambo(mac_address)
        self.debug = debug

    def start_flight(self):
        self.flying = True

        def fly():
            self.flying = True
            self.drone.connect(5)
            self.drone.smart_sleep(3)

            while self.flying:
                try:
                    c = self.commands.get(block=False)
                except:
                    self.drone.hover()
                    self.drone.smart_sleep(1)
                    continue

                if self.debug:
                    print(c)

                def done():
                    self.drone.safe_land(5)
                    self.flying = False
                code_to_command = {
                    0: (lambda: done()),
                    1: (lambda: self.drone.safe_takeoff(5)),  # takeoff
                    2: (lambda: self.drone.safe_land(5)),  # land
                    3: (lambda: self.drone.fly_direct(0, 10, 0, 0, 1)),  # forward
                    4: (lambda: self.drone.fly_direct(0, -10, 0, 0, 1)),  # backward
                    5: (lambda: self.drone.fly_direct(-10, 0, 0, 0, 1)),  # left
                    6: (lambda: self.drone.fly_direct(10, 0, 0, 0, 1)),  # right
                    7: (lambda: self.drone.fly_direct(0, 0, 0, 10)),  # up
                    8: (lambda: self.drone.fly_direct(0, 0, 0, -10)),  # down
                    9: (lambda: self.drone.turn_degrees(-45)),  # turn left
                    10: (lambda: self.drone.turn_degrees(45)),  # turn right
                    11: (lambda: self.drone.flip("front")),  # flip forward
                    12: (lambda: self.drone.flip("back")),  # flip backward
                    13: (lambda: self.drone.flip("right")),  # flip right
                    14: (lambda: self.drone.flip("left")),  # flip left
                }
                code_to_command[c.command_code]()
                self.drone.smart_sleep(3)

            self.drone.disconnect()
        t = Thread(target=fly)
        t.start()

    def send_command(self, command):
        if not self.flying:
            return False

        self.commands.put(command)
        return True

    def stop_flight(self):
        # self.send_command(<STOP COMMAND>)
        pass
