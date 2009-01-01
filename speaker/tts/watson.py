from ..speaker import Speaker

import pyaudio
import requests

class WatsonSpeaker(Speaker):
    RATE = 22050
    SAMPWIDTH = 2
    NCHANNELS = 1
    CHUNK = 2048
    ACCEPT = 'audio/wav'
    URL = 'https://stream.watsonplatform.net/text-to-speech/api'

    def __init__(self, config):
        self.username = config['username']
        self.password = config['password']
        self.voice    = config['voice']

    def speak(self, sentence):
        print "Transform '" + str(sentence) + "' into sound"
        req = requests.get(self.URL + "/v1/synthesize",
            auth=(self.username, self.password),
            params={'text': sentence, 'voice': self.voice, 'accept': self.ACCEPT},
            stream=True, verify=False
        )

        p = pyaudio.PyAudio()
        stream = p.open(format=p.get_format_from_width(self.SAMPWIDTH),
                        channels=self.NCHANNELS,
                        rate=self.RATE,
                        output=True)
        bytesRead = 0
        dataToRead = ''
        for data in req.iter_content(1):
            dataToRead += data
            bytesRead += 1
            if bytesRead % self.CHUNK == 0:
                stream.write(dataToRead)
                dataToRead = ''
        stream.stop_stream()
        stream.close()
        p.terminate()
