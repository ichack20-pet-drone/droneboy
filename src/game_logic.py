from command import Commands

class Game:
    def __init__(self, command_queue):
        self.satisfaction = 100
        self.command_queue = command_queue
        self.commands = Commands()
    
    def do_it(self):
        print(self.command_queue.get())
