from padatious import IntentContainer

class Commands:
    def __init__(self):
        startup = {
            'awaken': ['wake up', 'get up', 'rise and shine'],
            'home': ["I'm home"]
        }

        compliments = {
            'greeting': ["Hello", "It's good to see you", "How was your day", "hey", "hi"],
            'praise':   ["Who's a good boy?"],
            'affectionate': ["I missed you!"]
        }
        
        scoldings = {
            'chide': ["bad drone", "stop it"],
        }

        movements = {
            'up': ["move up", "go up", "fly up", "ascend"],
            'down': ["move down", "go down", "fly down", "descend"],
            'left': ["move left", "go left", "fly left"]
            'right': ["move right", "go right", "fly right"]
        }

        rotations = {
            'rotate_left': ["turn left", "face left", "look left"],
            'rotate_right':   ["turn right", "face right", "look right"],
        }

        flip = {
            'frontflip': ['somersault', 'front flip'],
            'backflip': ['backflip'],
            'sideflip': ['roll over', 'barrel roll']
        }

        play_dead = {
            'play_dead': ['play dead', 'crash'],
            'shoot': ['bang']
        }

        self.list = [startup, compliments, scoldings, movements, rotations, flip, play_dead]


class CommandDetector:
    def __init__(self, ):
        self.container = IntentContainer('intent_cache')
        self.commands = Commands()

    def add_command(self, commands):
        for c in self.commands.list:
            for intent, phrases in c.items():
                self.container.add_intent(intent, phrases)

    def train_commands(self):
        for c in self.commands.list:
            self.add_command(c)

        self.container.train()

    def calc_intent(self, text):
        return self.container.calc_intent(text)
