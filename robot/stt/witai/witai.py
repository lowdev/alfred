from ...robot import Robot
from witaiVoiceRequest import WitaiVoiceRequest
from .ear import Ear
import os
import threading

class WitaiRobot(Robot):
    BASE_URL = 'api.wit.ai'
    PATH = 'speech'

    def __init__(self, config, speaker, actions):
        super(WitaiRobot, self).__init__(config, speaker, actions)
        self.TOKEN = config['token']
        self.request = WitaiVoiceRequest(self.TOKEN, self.BASE_URL, self.PATH, {'v':'20160918'})
        self.audioConfig = {}
        self.audioConfig['channels'] = 1
        self.audioConfig['audio-rate'] = 44100
        self.audioConfig['audio-chunk'] = 512

    def name(self):
        return 'WitAi'

    def listen(self):       
        stopper = threading.Event()

        audioFd, writer = os.pipe()
        ear = Ear(self.audioConfig, stopper)
        ear.setWriter(writer)

        super(WitaiRobot, self).ding()
        ear.start()
        response = self.request.send(audioFd)

        result = response.get("result", None)
        if result:         
            print ("understand: " + result["resolvedQuery"])
            return (result["fulfillment"]["speech"], result["action"])   
        else:
           return (None, '')
