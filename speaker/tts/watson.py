from ..speaker import Speaker

import pyaudio
import requests
import time

from io import BytesIO
import soundfile as sf
from wave import Wave_read
import wave
import sys

class WatsonSpeaker(Speaker):
    RATE = 22050
    SAMPWIDTH = 2
    NCHANNELS = 1
    CHUNK = int(2048)
    ACCEPT = 'audio/wav'
    URL = 'https://stream.watsonplatform.net/text-to-speech/api'

    def __init__(self, config):
        self.username = config['username']
        self.password = config['password']
        self.voice    = config['voice']

    def speak(self, sentence):
        print "Transform '" + str(sentence) + "' into sound"
        response = requests.get(self.URL + "/v1/synthesize",
            auth=(self.username, self.password),
            params={'text': sentence, 'voice': self.voice, 'accept': self.ACCEPT},
            stream=True, verify=False
        )

        wave = Wave_read(BytesIO(response.content))

        p = pyaudio.PyAudio()
        stream = p.open(format=p.get_format_from_width(self.SAMPWIDTH),
                        channels=self.NCHANNELS,
                        rate=self.RATE,
                        output=True)

        stream.write(wave.readframes(wave.getnframes() / 2))

    def name(self):
        print 'Watson'

    def speakSreeam(self, sentence):
        print "Transform '" + str(sentence) + "' into sound"
        response = requests.get(self.URL + "/v1/synthesize",
            auth=(self.username, self.password),
            params={'text': sentence, 'voice': self.voice, 'accept': self.ACCEPT},
            stream=True, verify=False
        )

        p = pyaudio.PyAudio()
        stream = p.open(format=p.get_format_from_width(self.SAMPWIDTH),
                        channels=self.NCHANNELS,
                        rate=self.RATE,
                        output=True)

        f = BytesIO()
        turn = 1
        numberOfBytesForOneSecond = self.RATE * self.NCHANNELS * self.SAMPWIDTH
        dataToRead = None
        #response.iter_content(numberOfBytesForOneSecond/2)
        for data in response.iter_content():
            if data:
                f.write(data)
                print 'size: ' + str(len(data)) + ' byteSize: ' + str(len(f.getvalue()))
                         
                #if len(f.getvalue()) % (self.RATE * self.SAMPWIDTH) == 0:
                if len(f.getvalue()) > 10000 * turn: 
                    f.seek(0)
                    print 'f: ' + str(len(f.getvalue()))
                    wave_file = wave.open(f, 'rb')

                    # skip unwanted frames
                    #n_frames = int(turn/10 * wave_file.getframerate())
                    n_frames = int((turn-1) * len(f.getvalue()))
                    wave_file.setpos(n_frames)

                    turn += 1
                    frames = wave_file.readframes(numberOfBytesForOneSecond * turn)
                    stream.write(frames)
                    f.seek(10000 * turn)
                    wave_file.close()

        stream.stop_stream()
        stream.close()
        p.terminate()

