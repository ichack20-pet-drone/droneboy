import queue as q
import threading

from command import Commands
from game_logic import Game
from speech_detector import SpeechDetector


commands_queue = q.Queue()
speech_detector = SpeechDetector(commands_queue)

game = Game(commands_queue)
game_thread = threading.Thread(target=game.game_loop)
game_thread.start()

speech_thread = threading.Thread(target=speech_detector.start_stream)
speech_thread.start()
