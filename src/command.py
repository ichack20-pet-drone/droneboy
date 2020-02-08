from padatious import IntentContainer


class Commands:
    def __init__(self):
        startup = {
            'awaken': 'vocab/awaken.intent',
            'home': 'vocab/home.intent'
        }

        stop = {
            'stop': 'vocab/stop.intent'
        }

        compliments = {
            'greeting': 'vocab/greeting.intent',
            'praise': 'vocab/praise.intent',
            'affectionate': 'vocab/affectionate.intent'
        }

        scoldings = {
            'chide': 'vocab/chide.intent'
        }

        movements = {
            'up': 'vocab/up.intent',
            'down': 'vocab/down.intent',
            'left': 'vocab/left.intent',
            'right': 'vocab/right.intent'
        }

        rotations = {
            'rotate_left': 'vocab/rotate_left.intent',
            'rotate_right': 'vocab/rotate_right.intent'
        }

        flip = {
            'frontflip': 'vocab/frontflip.intent',
            'backflip': 'vocab/backflip.intent',
            'sideflip': 'vocab/sideflip.intent'
        }

        play_dead = {
            'play_dead': 'vocab/play_dead.intent',
            'shoot': 'vocab/shoot.intent'
        }

        self.family_list = [startup, stop, compliments, scoldings,
                     movements, rotations, flip, play_dead]
        self.family_names = ['startup', 'stop', 'compliments', 'scoldings',
                             'movements', 'rotations', 'flip', 'play_dead']

    def check_family(self, command):
        for i in range(len(self.family_list)):
            if command in self.family_list[i]:
                return self.family_names[i]
        return 'NOT FOUND'


class CommandDetector:
    def __init__(self, ):
        self.container = IntentContainer('intent_cache')
        self.commands = Commands()

    def add_command(self, commands):
        for c in self.commands.family_list:
            for intent, filename in c.items():
                self.container.load_file(intent, filename)

    def train_commands(self):
        for c in self.commands.family_list:
            self.add_command(c)

        self.container.train()

    def calc_intent(self, text):
        return self.container.calc_intent(text)
