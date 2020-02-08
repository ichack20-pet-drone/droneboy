from padatious import IntentContainer

class Commands:
    def __init__(self):
        startup = {
            'awaken': 'vocab/awaken.intent',
            'home': 'vocab/home.intent'
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

        self.list = [startup, compliments, scoldings, movements, rotations, flip, play_dead]


class CommandDetector:
    def __init__(self, ):
        self.container = IntentContainer('intent_cache')
        self.commands = Commands()

    def add_command(self, commands):
        for c in self.commands.list:
            for intent, filename in c.items():
                self.container.load_file(intent, filename)

    def train_commands(self):
        for c in self.commands.list:
            self.add_command(c)

        self.container.train()

    def calc_intent(self, text):
        return self.container.calc_intent(text)
