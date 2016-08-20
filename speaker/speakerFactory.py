from .tts import GoogleSpeaker
from .tts import WatsonSpeaker

class SpeakerFactory:
    @staticmethod
    def produce(config):
        configSTT = config['stt']
        if configSTT == 'watson':
           return WatsonSpeaker(config['watson'])

        return GoogleSpeaker()
        #raise Exception("Configuration STT error. Check your profile.yml") 
