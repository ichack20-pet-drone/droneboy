from padatious import IntentContainer

def add_stuff(stuff):
    for intent, phrases in stuff.items():
        container.add_intent(intent, phrases)

startup = {
        'awaken' : ['wake up', 'get up', 'rise and shine'],
        'home' : ["I'm home"]
        }

compliments = {
        'greeting': ["Hello", "It's good to see you", "How was your day"],
        'praise':   ["Who's a good boy?"],
        'affectionate': ["I missed you!"]
        }

flip = {
        'frontflip' : ['somersault', 'front flip'],
        'backflip' : ['backflip'],
        'sideflip' : ['roll over', 'barrel roll']
        }
        
play_dead = {
        'play_dead' : ['play dead', 'crash'],
        'shoot' : ['bang']
        }

container = IntentContainer('intent_cache')
add_stuff(startup)
add_stuff(compliments)
add_stuff(flip)
add_stuff(play_dead)
container.train()

print(container.calc_intent("It's nice to see you"))
print(container.calc_intent("Time to get up!"))
print(container.calc_intent("do a barrel roll"))
print(container.calc_intent("boom"))

