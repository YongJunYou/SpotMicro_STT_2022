from __future__ import division

import re
import sys
import os

from google.cloud import speech
os.environ['GOOGLE_APPLICATION_CREDENTIALS']=r"/home/@put yourname/SpotMicro_STT/Common/@put your_speechtotext_key.json"
import pyaudio
from six.moves import queue

# Audio recording parameters
RATE = 16000
CHUNK = int(RATE / 10)  # 100ms

from multiprocessing import Process, Queue
from Common.stt_test1 import MicrophoneStream

stop_status_offset = {'Wait': False } #수정됨

class MicInterrupt(object): 

    def __init__(self): 
        # Calculate Offset based on Key Status
        self.stop_status = Queue()
        self.stop_status.put(stop_status_offset)

    def stop(self):
        result_dict = self.stop_status.get()
        result_dict['Wait'] = True
        self.stop_status.put(result_dict)
    
    def go(self):
        result_dict = self.stop_status.get()
        result_dict['Wait'] = False
        self.stop_status.put(result_dict)

    def micInterrupt(self, id, stop_status):
        language_code = 'ko-KR'  # a BCP-47 language tag

        client = speech.SpeechClient()
        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=RATE,
            language_code=language_code)
        streaming_config = speech.StreamingRecognitionConfig(
            config=config,
            interim_results=True)

        with MicrophoneStream(RATE, CHUNK) as stream:
            audio_generator = stream.generator()
            requests = (speech.StreamingRecognizeRequest(audio_content=content)
                        for content in audio_generator)

            responses = client.streaming_recognize(streaming_config, requests)

            # Now, put the transcription responses to use.
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

                    if transcript.split()[-1] == '앉아':
                        print('앉겠습니다\n')
                    elif transcript.split()[-1] == '일어서':
                        print('일어서겠습니다\n')
                    elif transcript.split()[-1] == '손':
                        print('손을 내민다\n')
                    elif transcript.split()[-1] == '기다려' or transcript.split()[-1] == '정지':# 개한테 말하듯이 단호하게 해야 잘됨
                        print('기다려\n')
                        self.stop()
                    elif transcript.split()[-1] == '가' or transcript.split()[-1] == '출발': # 개한테 말하듯이 단호하게 해야 잘됨
                        print('가겠습니다\n')
                        self.go()

                else:
                    words = transcript + overwrite_chars
                    print(words)
                    # Exit recognition if any of the transcribed phrases could be
                    # one of our keywords.
                    if re.search(r'\b(exit|quit)\b', transcript, re.I):
                        print('Exiting..')
                        break

                    num_chars_printed = 0


