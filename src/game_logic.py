from command import Commands

class Game:
    def __init__(self, command_queue):
        self.session_list = []
        self.command_queue = command_queue
        self.commands = Commands()
    
    def game_loop(self): 
    # pops actions from the queue every x milliseconds and passes them to the existing session
        pass

    def start_game(self):
    # Starts a session and adds it to the session list once it terminates
        pass

    def calc_game_stats(self):
    # For twitter stuff after the sessions finish
        pass

    def tweet_stats(self):
    # For twitter stuff after the sessions finish
        pass

    # REMOVE ME
    def do_it(self):
        while True:
            item = self.command_queue.get()
            print('get')
            print(item)


class Session: 
    def __init__(self):
        self.player_name = ""
        self.isActive = False
        self.satisfaction = 40
