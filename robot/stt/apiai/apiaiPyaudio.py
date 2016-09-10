try:
    import apiai 
except ImportError:
    sys.path.append(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir)
    )
    import apiai

import thread
import pyaudio
import time
import json
from ..vad import ApiaiVAD

class ApiaiPyaudioEar(object):
    RATE = 44100
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    CHUNK = 512

    def __init__(self, requester):
        super(ApiaiPyaudioEar, self).__init__()
        self.resampler = apiai.Resampler(source_samplerate=self.RATE)
        self.vad = ApiaiVAD()
        self.stream = None
        self.requester = requester
        self.pyAudio = None
    
    def input_thread(self, L):
        raw_input()
        L.append(None)
    
    def getReady(self):
        self.vad.reset()
        self.vad = ApiaiVAD()

        def callback(in_data, frame_count, time_info, status):
            frames, data = self.resampler.resample(in_data, frame_count)
            state = self.vad.processFrame(frames)
            self.requester.send(data)
            if (state == 1):
               return in_data, pyaudio.paContinue
            else:
               return in_data, pyaudio.paComplete
       
        self.pyAudio = pyaudio.PyAudio()
        self.stream = self.pyAudio.open(format=self.FORMAT,
                    channels=self.CHANNELS,
                    rate=self.RATE,
                    input=True,
                    output=False,
                    frames_per_buffer=self.CHUNK,
                    stream_callback=callback)
    
    def listen(self):
        self.stream.start_stream()
        print ("Say! Press enter for stop audio recording.")
        try:
           L = []
           thread.start_new_thread(self.input_thread, (L,))
           while self.stream.is_active() and len(L) == 0:
             time.sleep(0.1)
        except Exception:
           raise
        except KeyboardInterrupt:
           pass
        self.stream.stop_stream()
        self.stream.close()
        self.pyAudio.terminate()

        return self.requester.getResponse()


