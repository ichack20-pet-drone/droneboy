from command import Commands

class Game:
    def __init__(self, command_queue):
        self.satisfaction = 100
        self.command_queue = command_queue
        self.commands = Commands()
    
    def do_it(self):
        while True:
            item = self.command_queue.get()
            print('get')
            print(item)
