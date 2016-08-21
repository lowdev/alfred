from .tts import GoogleSpeaker
from .tts import WatsonSpeaker

class SpeakerFactory:
    @staticmethod
    def produce(config):
        configTTS = config['tts']
        if configTTS == 'watson':
           return WatsonSpeaker(config['watson'])

        return GoogleSpeaker()
        #raise Exception("Configuration STT error. Check your profile.yml") 

