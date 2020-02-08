from queue import Queue
from pyparrot.Minidrone import Mambo

class Command():
    def __init__(self):
        pass


class DroneController():

    def __init__(self, mac_address, debug=False):
        self.flying = False
        self.commands = Queue()
        self.drone = Mambo(mac_address)
        self.debug = debug

    def start_flight(self):
        self.flying = True

        # start flying thread

    def send_command(self, command):
        if not self.flying:
            return False
        
        self.commands.put(command)
        return True

    def stop_flight(self):
        # self.send_command(<STOP COMMAND>)
        pass

    
    

