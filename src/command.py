from padatious import IntentContainer

startup = {
    'awaken': ['wake up', 'get up', 'rise and shine'],
    'home': ["I'm home"]
}

compliments = {
    'greeting': ["Hello", "It's good to see you", "How was your day", "hey", "hi"],
    'praise':   ["Who's a good boy?"],
    'affectionate': ["I missed you!"]
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

commands = [startup, compliments, flip, play_dead]


class CommandDetector:
    def __init__(self):
        self.container = IntentContainer('intent_cache')

    def add_command(self, commands):
        for intent, phrases in commands.items():
            self.container.add_intent(intent, phrases)

    def train_commands(self):
        for c in commands:
            self.add_command(c)

        self.container.train()

    def calc_intent(self, text):
        return self.container.calc_intent(text)
