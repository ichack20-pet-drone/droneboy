import re
import sys

from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types

from mic_stream import MicrophoneStream


class SpeechDetector(object):
    def __init__(self, language_code='en-US'):
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

    def listen_print_loop(self, responses):
        """
        Iterates through server responses and prints them.

        The responses passed is a generator that will block until a response
        is provided by the server.

        Each response may contain multiple results, and each result may contain
        multiple alternatives; for details, see https://goo.gl/tjCPAU.  Here we
        print only the transcription for the top alternative of the top result.

        In this case, responses are provided for interim results as well. If the
        response is an interim one, print a line feed at the end of it, to allow
        the next result to overwrite it, until the response is a final one. For the
        final one, print a newline to preserve the finalized transcription.
        """

        num_chars_printed = 0
        for response in responses:
            if not response.results:
                continue

            # The `results` list is consecutive. For streaming, we only care about
            # the first result being considered, since once it's `is_final`, it
            # moves on to considering the next utterance.
            result = response.results[0]
            if not result.alternatives:
                continue

            # Display the transcription of the top alternative.
            transcript = result.alternatives[0].transcript

            # Display interim results, but with a carriage return at the end of the
            # line, so subsequent lines will overwrite them.
            #
            # If the previous result was longer than this one, we need to print
            # some extra spaces to overwrite the previous result
            overwrite_chars = ' ' * (num_chars_printed - len(transcript))

            if not result.is_final:
                sys.stdout.write(transcript + overwrite_chars + '\r')
                sys.stdout.flush()

                num_chars_printed = len(transcript)

            else:
                print(transcript + overwrite_chars)

                # Exit recognition if any of the transcribed phrases could be
                # one of our keywords.
                if re.search(r'\b(exit|quit)\b', transcript, re.I):
                    print('Exiting..')
                    break

                num_chars_printed = 0

    def get_text(self):
        with MicrophoneStream(self.RATE, self.CHUNK) as stream:
            audio_generator = stream.generator()
            requests = (types.StreamingRecognizeRequest(audio_content=content)
                        for content in audio_generator)

            responses = self.client.streaming_recognize(
                self.streaming_config, requests)

            # Now, put the transcription responses to use.
            self.listen_print_loop(responses)


if __name__ == "__main__":
    sd = SpeechDetector()
    sd.get_text()
