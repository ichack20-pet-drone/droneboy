import time
import json
import drone_control as dc
import drone_control.commands as dc_commands
from command import Commands as PetCommands

START_SATISFACTION = 50
MAX_SATISFACTION = 120

class Session:
    def __init__(self, p_name, command_queue):
        self.player_name = p_name
        self.command_queue = command_queue
        self.satisfaction = START_SATISFACTION
        self.controller = dc.get_drone_controller(mock=True)
        self.pet_commands = PetCommands()
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
        self.satisfaction += magnitude
        self.satisfaction = min(self.satisfaction, MAX_SATISFACTION)

    def decrease_satisfaction(self, magnitude):
        self.satisfaction -= magnitude
        self.satisfaction = max(self.satisfaction, 0)
    
    def multiply_satisfaction(self, scalar):
        self.satisfaction *= scalar
        self.satisfaction = min(self.satisfaction, MAX_SATISFACTION)

    def process_basic(self, command):
        # Don't need to do anything
        pass

    def process_emotion(self, command):
        family = self.pet_commands.check_family(command)
        if family == 'compliments':
            self.increase_satisfaction(15)
        if family == 'scoldings':
            self.multiply_satisfaction(0.8)

    def process_actions(self, command):
        tr, req = self.translate_action[command]
        if req <= self.satisfaction:
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
        print(F'Satisfaction: {self.satisfaction}')

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
            
            self.command_processing(c)
        
        self.controller.send_command(dc_commands.Stop())
        print('Session over')


class Game:
    def __init__(self, command_queue):
        self.session_list = []
        self.command_queue = command_queue
        self.commands = PetCommands()

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
        print('start_session')      

        print("Tell me your name!")
        # TODO: Query matching HERE
        name = self.command_queue.get()
        session = Session(name, self.command_queue)
        session.session_loop()
        
    def calc_game_stats(self):
        # For twitter stuff after the sessions finish
        pass

    def tweet_stats(self):
        # For twitter stuff after the sessions finish
        pass
