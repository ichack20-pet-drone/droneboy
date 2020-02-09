import time
import json
import requests
import drone_control as dc
import drone_control.commands as dc_commands
from command import Commands as PetCommands

START_SATISFACTION = 50
MAX_SATISFACTION = 120
SERVER_ADDR = "http://localhost:23333/api"

class Session:
    def __init__(self, p_name, command_queue):
        self.player_name = p_name
        self.command_queue = command_queue
        self.controller = dc.get_drone_controller(mock=True)
        self.pet_commands = PetCommands()
        
        with open("players.json", "r+") as jsonfile:
            self.file = json.load(jsonfile)

        self.play_data = {
            'satisfaction' : START_SATISFACTION,
            'commands' : 0,
            'compliments' : 0,
            'scoldings' : 0
        }

        self.translate_action = {
            'takeoff': (dc_commands.Takeoff, 20),
            'up': (dc_commands.Up, 30),
            'down': (dc_commands.Down, 30),
            'left': (dc_commands.Left, 30),
            'right': (dc_commands.Right, 30),
            'forward': (dc_commands.Forward, 30),
            'backward': (dc_commands.Backward, 30),
            'land': (dc_commands.Land, 0),
            'rotate_left': (dc_commands.TurnLeft, 40),
            'rotate_right': (dc_commands.TurnRight, 40),
            'frontflip': (dc_commands.FlipForward, 50),
            'backflip': (dc_commands.FlipBackward, 50),
            'sideflip': (dc_commands.FlipRight, 50)
        }

    def increase_satisfaction(self, magnitude):
        self.play_data['satisfaction'] += magnitude
        self.play_data['satisfaction'] = min(self.play_data['satisfaction'], MAX_SATISFACTION)
        # res = requests.post(url = SERVER_ADDR, data = self.play_data)

    def decrease_satisfaction(self, magnitude):
        self.play_data['satisfaction'] -= magnitude
        self.play_data['satisfaction'] = max(self.play_data['satisfaction'], 0)
        # res = requests.post(url = SERVER_ADDR, data = self.play_data)
    
    def multiply_satisfaction(self, scalar):
        self.play_data['satisfaction'] *= scalar
        self.play_data['satisfaction'] = min(self.play_data['satisfaction'], MAX_SATISFACTION)
        # res = requests.post(url = SERVER_ADDR, data = self.play_data)

    def process_basic(self, command):
        # Don't need to do anything
        pass

    def process_emotion(self, command):
        family = self.pet_commands.check_family(command)
        if family == 'compliments':
            self.play_data['compliments'] += 1
            self.increase_satisfaction(15)
        if family == 'scoldings':
            self.play_data['scoldings'] += 1
            self.multiply_satisfaction(0.8)

    def process_actions(self, command):
        tr, req = self.translate_action[command]
        if req <= self.play_data['satisfaction']:
            self.controller.send_command(tr())
        self.decrease_satisfaction(5)

    def process_game(self, command):
        # TODO: do something later
        pass

    def command_processing(self, command):
        family_class = self.pet_commands.check_family_class(command)
        if family_class == 'basic':
            self.process_basic(command)
        if family_class == 'emotion':
            self.process_emotion(command)
        if family_class == 'actions':
            self.process_actions(command)
        if family_class == 'game':
            self.process_game(command)
        print(F"Satisfaction: {self.play_data['satisfaction']}")

    def session_loop(self):
        input('Are you ready kids??')

        self.start_time = time.time()
        
        # Empty the queue
        while not self.command_queue.empty():
            self.command_queue.get()

        self.controller.start_flight()
        self.controller.send_command(dc_commands.Takeoff())

        while time.time() - self.start_time <= 180:
            try:
                c = self.command_queue.get(block=False).name
            except: 
                continue # Check me later
            if c == 'stop':
                break
            
            self.play_data['commands'] += 1
            self.command_processing(c)
            # TODO: send command here
        
        self.controller.send_command(dc_commands.Stop())

        # Dump player data into file
        self.file[self.player_name] = self.play_data
        
        with open("players.json", "r+") as jsonfile:
            jsonfile.seek(0)
            json.dump(self.file, jsonfile)
            jsonfile.truncate()

        print('Session over')


class Game:
    def __init__(self, command_queue):
        self.session_list = []
        self.command_queue = command_queue
        self.commands = PetCommands()
        # self.player_data = 

    def game_loop(self):
        # pops actions from the queue every x milliseconds and passes them to the existing session
        while True:
            try:
                command = self.command_queue.get(block=False).name
            except: 
                continue # Check me later
            print(command)
            if (self.commands.check_family(command) == 'startup'):
                # Flush the queue
                while not self.command_queue.empty():
                    self.command_queue.get()
                self.start_session()

    def start_session(self):
        # Starts a session and adds it to the session list once it terminates
        print("Tell me your name!")
        intent = self.command_queue.get()

        while(intent.name != "name"):
            intent = self.command_queue.get()

        name = intent.matches['name']

        print(f"Starting session with player name: {name}")
        session = Session(name, self.command_queue)
        session.session_loop()
        
    def calc_game_stats(self):
        # For twitter stuff after the sessions finish
        pass

    def tweet_stats(self):
        # For twitter stuff after the sessions finish
        pass
