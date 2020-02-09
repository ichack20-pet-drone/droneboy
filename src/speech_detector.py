import re
import sys

from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types

from mic_stream import MicrophoneStream
from command import CommandDetector


class SpeechDetector:
    def __init__(self, command_queue, language_code='en-US'):
        # Audio recording parameters
        self.RATE = 16000
        self.CHUNK = int(self.RATE / 10)  # 100ms

        self.client = speech.SpeechClient()

        self.config = types.RecognitionConfig(
            encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=self.RATE,
            language_code=language_code)
        self.streaming_config = types.StreamingRecognitionConfig(
            config=self.config,
            interim_results=True)

        self.command_detector = CommandDetector()
        self.command_detector.train_commands()

        self.queue = command_queue

    def listen_print_loop(self, responses):
        for response in responses:
            if not response.results:
                continue

            result = response.results[0]
            if not result.alternatives:
                continue
            transcript = result.alternatives[0].transcript
            if result.is_final:
                intent = self.command_detector.calc_intent(transcript)
                print(intent)
                self.queue.put(intent)

    def start_stream(self):
        with MicrophoneStream(self.RATE, self.CHUNK) as stream:
            audio_generator = stream.generator()
            requests = (types.StreamingRecognizeRequest(audio_content=content)
                        for content in audio_generator)

            responses = self.client.streaming_recognize(
                self.streaming_config, requests)

            self.listen_print_loop(responses)
