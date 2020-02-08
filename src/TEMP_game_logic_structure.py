from command import Commands
import time

class Game:
    def __init__(self, command_queue):
        self.session_list = []
        self.command_queue = command_queue
        self.commands = Commands()
    
    def start_game(self):
        pass

    def calc_game_stats(self):
        pass

    def tweet_stats(self):
        pass


class Session: 
    def __init__(self):
        self.player_name = ""
        self.isActive = False
        self.satisfaction = 40


