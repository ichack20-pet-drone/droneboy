import queue as q

from command import Commands
from game_logic import Game
from speech_detector import SpeechDetector


commands_queue = q.Queue()
speech_detector = SpeechDetector(commands_queue)

speech_detector.start_stream()
