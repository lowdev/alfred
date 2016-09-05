from ..robot import Robot

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

from .vad import ApiaiVAD
from .ear import PyaudioEar

class ApiRobot(Robot):
    def __init__(self, config, speaker, actions):
        super(ApiRobot, self).__init__(config, speaker, actions)
        self.CLIENT_ACCESS_TOKEN = config['client_access_token']
        self.ai = apiai.ApiAI(self.CLIENT_ACCESS_TOKEN)

    def name(self):
        return 'ApiAi'

    def listen(self):
        request = self.ai.voice_request()
        request.lang = 'en' # optional, default value equal 'en'
        ear = PyaudioEar(request)
        ear.getReady()
        super(ApiRobot, self).ding()
        response = ear.listen()

        result = response["result"]
        if result:         
            print ("understand: " + result["resolvedQuery"])
            return (result["fulfillment"]["speech"], result["action"])   
        else:
           return None
