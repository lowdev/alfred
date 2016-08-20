from ..speaker import Speaker

import pyaudio
import requests
import time

from io import BytesIO
import soundfile as sf
from wave import Wave_read
import wave

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


        f = BytesIO()
        for data in response.iter_content():
            if data:
                f.write(data)
                
        f.seek(0)
        wave_file = wave.open(f, 'rb')
        #wave_file = Wave_read(f.content)
        #seems there is a lot of empty nFrames
        print 'frame: ' + str(wave_file.getnframes())
        frames = wave_file.readframes(wave_file.getnframes()/2)

        proc_audio = pyaudio.PyAudio()
        stream = proc_audio.open(
            format=proc_audio.get_format_from_width(wave_file.getsampwidth()),
            channels=wave_file.getnchannels(),
            rate=wave_file.getframerate(),
            output=True
        )      
        stream.write(frames)

        stream.stop_stream()
        stream.close()
 
        proc_audio.terminate()
        wave_file.close()

#        p = pyaudio.PyAudio()
#        stream = p.open(format=p.get_format_from_width(self.SAMPWIDTH),
#                        channels=self.NCHANNELS,
#                        rate=self.RATE,
#                        output=True)
       
#        silence = "0" * 3072 
#        bytesRead = 0
#        dataToRead = ''
#        for data in req.iter_content(8096):
#            dataToRead += data
#            bytesRead += 1
#            if bytesRead % self.CHUNK == 0:
#                print (str(stream.get_write_available())
#                stream.write(dataToRead)
#                dataToRead = ''

#        stream.stop_stream()
#        stream.close()
#        p.terminate()
