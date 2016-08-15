from ..body import Body

import os
import sys

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

CHUNK = 512
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 2

CLIENT_ACCESS_TOKEN = '5fa81928957d47268b724df067a4bd5b'

class ApiBody(Body):
    def __init__(self, mouth):
        #Todo find a way to not initialize here
        self.interrupted = False
        self.mouth = mouth

    def speak(self, text):
        self.mouth.speak(text)

    def listen(self):
        resampler = apiai.Resampler(source_samplerate=RATE)

        vad = apiai.VAD()

        ai = apiai.ApiAI(CLIENT_ACCESS_TOKEN)

        request = ai.voice_request()

        request.lang = 'en'  # optional, default value equal 'en'

        def callback(in_data, frame_count, time_info, status):
            frames, data = resampler.resample(in_data, frame_count)
            state = vad.processFrame(frames)
            request.send(data)

            if (state == 1):
               return in_data, pyaudio.paContinue
            else:
               return in_data, pyaudio.paComplete
        
        def input_thread(L):
            raw_input()
            L.append(None)
       
        p = pyaudio.PyAudio()

        stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    output=False,
                    frames_per_buffer=CHUNK,
                    stream_callback=callback)

        stream.start_stream()

        print ("Say! Press enter for stop audio recording.")

        try:
           L = []
           thread.start_new_thread(input_thread, (L,))

           while stream.is_active() and len(L) == 0:
             time.sleep(0.1)

        except Exception:
           raise
        except KeyboardInterrupt:
           pass

        stream.stop_stream()
        stream.close()
        p.terminate()

        print ("Wait for response...")
        httpResponse = request.getresponse()
        response = json.loads(httpResponse.read())
        
        print ("understand: " + response["result"]["resolvedQuery"])
        print ("response: " + response["result"]["fulfillment"]["speech"])
        return response["result"]["fulfillment"]["speech"]   
