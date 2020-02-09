import time
import json
import random
import requests
from playsound import playsound
import drone_control as dc
import drone_control.commands as dc_commands
from command import Commands as PetCommands

START_SATISFACTION = 50
MAX_SATISFACTION = 120
SERVER_ADDR = "http://localhost:23333/api"
STATS_API = SERVER_ADDR + "/stats"
LOG_API = SERVER_ADDR + "/message"


def _send_server_message(msg):
    print(F"Sending: {msg}")
    requests.post(url = LOG_API, data = {"message": msg})


class Session:
    def __init__(self, p_name, command_queue):
        self.player_name = p_name
        self.command_queue = command_queue
        self.consec_complement = 0
        self.controller = dc.get_drone_controller(mock=True)
        self.pet_commands = PetCommands()
        
        with open("players.json", "r+") as jsonfile:
            self.file = json.load(jsonfile)

        self.play_data = {
            'playerName': self.player_name,
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
            'play_dead': (dc_commands.Land, 30),
            'rotate_left': (dc_commands.TurnLeft, 40),
            'rotate_right': (dc_commands.TurnRight, 40),
            'frontflip': (dc_commands.FlipForward, 50),
            'backflip': (dc_commands.FlipBackward, 50),
            'sideflip': (dc_commands.FlipRight, 50)
        }

        self.update_server_stats()

    def update_server_stats(self):
        requests.post(url = STATS_API, data = self.play_data)

    def increase_satisfaction(self, magnitude):
        self.play_data['satisfaction'] += magnitude
        self.play_data['satisfaction'] = min(self.play_data['satisfaction'], MAX_SATISFACTION)
        self.update_server_stats()

    def decrease_satisfaction(self, magnitude):
        self.play_data['satisfaction'] -= magnitude
        self.play_data['satisfaction'] = max(self.play_data['satisfaction'], 0)
        self.update_server_stats()
    
    def multiply_satisfaction(self, scalar):
        self.play_data['satisfaction'] *= scalar
        self.play_data['satisfaction'] = min(self.play_data['satisfaction'], MAX_SATISFACTION)
        self.update_server_stats()

    def process_basic(self, command):
        # Don't need to do anything
        pass

    def process_emotion(self, command):
        family = self.pet_commands.check_family(command)
        if family == 'compliments':
            self.consec_complement += 1
            
            if self.consec_complement > 1 and random.randint(0, 1) == 1:
                self.play_data['scoldings'] += 1
                self.multiply_satisfaction(0.6)
            else:
                self.play_data['scoldings'] += 1
                self.increase_satisfaction(15)

        if family == 'scoldings':
            self.consec_complement = False
            self.play_data['scoldings'] += 1
            self.multiply_satisfaction(0.8)

    def process_actions(self, command):
        tr, req = self.translate_action[command]
        if req <= self.play_data['satisfaction']:
            self.controller.send_command(tr())
        self.decrease_satisfaction(5)

    def process_game(self, command):
        # Play dead handling code
        if command == "play_dead":            
            # Handle the play dead
            self.process_actions(command)
            intent = self.command_queue.get(block=True).name

            while (not 'awaken' == intent):
                intent = self.command_queue.get(block=True).name
            self.process_actions('takeoff')


    def command_processing(self, command):
        family_class = self.pet_commands.check_family_class(command)
        if family_class == 'basic':
            self.process_basic(command)
        if family_class == 'emotion':
            self.process_emotion(command)
        if family_class == 'actions':
            self.consec_complement = False
            self.process_actions(command)
        if family_class == 'game':
            self.consec_complement = False
            self.process_game(command)
        if family_class == 'name':
            pass
        print(F"Satisfaction: {self.play_data['satisfaction']}")

    def session_loop(self):
        self.start_time = time.time()
        
        # Empty the queue
        while not self.command_queue.empty():
            self.command_queue.get()

        self.controller.start_flight()
        self.controller.send_command(dc_commands.Takeoff())

        while time.time() - self.start_time <= 180:
            try:
                c = self.command_queue.get(block=False).name
                _send_server_message(F'Heard command: {c}')
            except: 
                continue # Check me later
            if c == 'stop':
                playsound("soundfiles/Good_Bye_Female.mp3")
                break
            
            self.play_data['commands'] += 1
            self.command_processing(c)
       
        self.controller.send_command(dc_commands.Stop())

        # Dump player data into file
        self.file[self.player_name] = self.play_data
        
        with open("players.json", "r+") as jsonfile:
            jsonfile.seek(0)
            json.dump(self.file, jsonfile)
            jsonfile.truncate()

        _send_server_message('Session over')


class Game:
    def __init__(self, command_queue):
        self.session_list = []
        self.command_queue = command_queue
        self.commands = PetCommands()
        # self.player_data = 

    def game_loop(self):
        _send_server_message('Say "Wake up" to start')
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
        _send_server_message("Tell me your name!")

        found_name = False
        while not found_name:
            intent = self.command_queue.get()
            if intent.name != "name":
                continue
            if 'name' not in intent.matches:
                continue
            name = intent.matches['name']
            found_name = True

        msg = self.generate_greeting(name)
        _send_server_message(msg)

        print(f"Starting session with player name: {name}")
        playsound('soundfiles/Good_Morning_Female.mp3')
        session = Session(name, self.command_queue)
        session.session_loop()

        self.session_list.append(session)

    def generate_greeting(self, name):
        last_session = None

        for s in self.session_list:
            if s.player_name == name:
                last_session = s

        if last_session == None:
            return F"Hi {name}, nice to meet you!"

        last_stats = last_session.play_data
        # satisfaction, commands, compliments, scoldings
        if last_stats['satisfaction'] > 80:
            best_friend = "no one"
            highest_sat = 0
            for s in self.session_list:
                if s.play_data['satisfaction'] >= highest_sat:
                    best_friend = s.player_name

            if name == best_friend:
                return F"{name}? Great! You're my best friend!"
            else:
                return F"Great to see you again {name}!"

        if last_stats['satisfaction'] < 30:
            return F"{name}? I was hoping you wouldn't come back"

        if last_stats['compliments'] > 10:
            return F"Aww {name}, you were so nice to me last time"

        if last_stats['scoldings'] > 5:
            return F"I don't like you {name}, you're mean"

        if last_stats['commands'] > 10:
            return F"Hi coach {name}"

        return F"Nice to see you again {name}"


    def calc_game_stats(self):
        # For twitter stuff after the sessions finish
        pass

    def tweet_stats(self):
        # For twitter stuff after the sessions finish
        pass
