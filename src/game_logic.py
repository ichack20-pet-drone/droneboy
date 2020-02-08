import time
import drone_control as dc
import drone_control.commands as dc_commands
from command import Commands as PetCommands

START_SATISFACTION = 40

class Session:
    def __init__(self, p_name, command_queue):
        self.player_name = p_name
        self.command_queue = command_queue
        self.satisfaction = START_SATISFACTION
        self.controller = dc.get_drone_controller()
        self.translate_commands = {
            "": (dc_commands.Land, 0),
            "stop": (dc_commands.Stop, 0),
            "takeoff": (dc_commands.Takeoff, 0),
            "land": (dc_commands.Land, 0),
            "forward": (dc_commands.Forward, 0),
            "backward": (dc_commands.Backward, 0),
            "left": (dc_commands.Left, 0),
            "right": (dc_commands.Right, 0),
        }

    def session_loop(self):
        input("Are you ready kids?? ") # aye aye
        self.controller.start_flight()
        self.controller.send_command(dc_commands.Takeoff())

        # End session when this loop is broken, either by command or 3 mins
        while True:
            try:
                c = self.command_queue.get(block=False)
            except: 
                continue # Check me later
            tr, req = self.translate_commands[c]
            if req < self.satisfaction:
                self.controller.send_command(tr())
            if c == "stop":
                break

        
        print("Flight over")


class Game:
    def __init__(self, command_queue):
        self.session_list = []
        self.command_queue = command_queue
        self.commands = PetCommands()

    def game_loop(self):
        # pops actions from the queue every x milliseconds and passes them to the existing session
        while True:
            try:
                command = self.command_queue.get(block=False)
            except: 
                continue # Check me later
            print(command)
            if (self.commands.check_family(command) == 'startup'):
                self.start_session()

    def start_session(self):
        # Starts a session and adds it to the session list once it terminates
        print('start_session')
        session = Session("Kevin", self.command_queue)
        session.session_loop()
        
    def calc_game_stats(self):
        # For twitter stuff after the sessions finish
        pass

    def tweet_stats(self):
        # For twitter stuff after the sessions finish
        pass
