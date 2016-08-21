from ..robot import Robot

from  bing_voice import *
import webrtcvad
import collections
import sys
import signal
import pyaudio

class BingRobot(Robot):
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000
    CHUNK_DURATION_MS = 30  # supports 10, 20 and 30 (ms)
    PADDING_DURATION_MS = 1000
    CHUNK_SIZE = int(RATE * CHUNK_DURATION_MS / 1000)
    CHUNK_BYTES = CHUNK_SIZE * 2
    NUM_PADDING_CHUNKS = int(PADDING_DURATION_MS / CHUNK_DURATION_MS)
    NUM_WINDOW_CHUNKS = int(240 / CHUNK_DURATION_MS)

    def __init__(self, config, speaker, actions):
        super(BingRobot, self).__init__(config, speaker, actions)
        self.BING_KEY = config['key']

    def listen(self):
        vad = webrtcvad.Vad(2)
        bing = BingVoice(self.BING_KEY)

        pa = pyaudio.PyAudio()
        stream = pa.open(format=self.FORMAT,
                           channels=self.CHANNELS,
                           rate=self.RATE,
                           input=True,
                           start=False,
                           # input_device_index=2,
                           frames_per_buffer=self.CHUNK_SIZE)


        got_a_sentence = False
        leave = False

        def handle_int(sig, chunk):
            global leave, got_a_sentence

            leave = True
            got_a_sentence = True
  
        signal.signal(signal.SIGINT, handle_int)

        while not leave:
            ring_buffer = collections.deque(maxlen=self.NUM_PADDING_CHUNKS)
            triggered = False
            voiced_frames = []
            ring_buffer_flags = [0] * self.NUM_WINDOW_CHUNKS
            ring_buffer_index = 0
            buffer_in = ''

            print("* recording")
            stream.start_stream()
            while not got_a_sentence and not leave:
                chunk = stream.read(self.CHUNK_SIZE)
                active = vad.is_speech(chunk, self.RATE)
                sys.stdout.write('1' if active else '0')
                ring_buffer_flags[ring_buffer_index] = 1 if active else 0
                ring_buffer_index += 1
                ring_buffer_index %= self.NUM_WINDOW_CHUNKS
                if not triggered:
                    ring_buffer.append(chunk)
                    num_voiced = sum(ring_buffer_flags)
                    if num_voiced > 0.5 * self.NUM_WINDOW_CHUNKS:
                        sys.stdout.write('+')
                        triggered = True
                        voiced_frames.extend(ring_buffer)
                        ring_buffer.clear()
                else:
                    voiced_frames.append(chunk)
                    ring_buffer.append(chunk)
                    num_unvoiced = self.NUM_WINDOW_CHUNKS - sum(ring_buffer_flags)
                    if num_unvoiced > 0.9 * self.NUM_WINDOW_CHUNKS:
                        sys.stdout.write('-')
                        triggered = False
                        got_a_sentence = True

                sys.stdout.flush()

            sys.stdout.write('\n')
            data = b''.join(voiced_frames)
    
            stream.stop_stream()
            print("* done recording")

            # recognize speech using Microsoft Bing Voice Recognition
            try:
                text = bing.recognize(data, language='en-US')
                print('Bing:' + text.encode('utf-8'))
            except UnknownValueError:
                print("Microsoft Bing Voice Recognition could not understand audio")
            except RequestError as e:
                print("Could not request results from Microsoft Bing Voice Recognition service; {0}".format(e))
        
            got_a_sentence = False
        
        stream.close()
