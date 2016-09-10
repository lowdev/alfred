from ...robot import Robot
from ..ear import PyaudioEar
from .watsonRequester import  WatsonRequester

from websocket import create_connection
from base64 import b64encode
import requests
import json

class WatsonRobot(Robot):
    def __init__(self, config, speaker, actions):
        super(WatsonRobot, self).__init__(config, speaker, actions)
        self.model = 'en-US_BroadbandModel'
        self.server = 'stream.watsonplatform.net'
        self.hostname = 'https://' + self.server + '/'
        self.url = "wss://" + self.server + "/speech-to-text/api/v1/recognize?model=" + self.model
        self.username = config['username']
        self.password = config['password']

    def name(self):
        return 'Watson'

    def listen(self):
        token = self.token()

        ws = create_connection(self.url + '&watson-token=' + token)

        data = {"action": "start", "content-type": "audio/l16;rate=44100", "continuous": True, "interim_results": True,
                "inactivity_timeout": 600}
        data['word_confidence'] = True
        data['timestamps'] = True
        data['max_alternatives'] = 3
        ws.send(json.dumps(data).encode('utf8'))
        #ws.send("{\"action\": \"start\", \"content-type\": \"audio/l16;rate=44100\"}")
        result =  ws.recv()
        print "Received '%s'" % result

        requester = WatsonRequester(ws)
        ear = PyaudioEar(requester)
        ear.getReady()
        super(WatsonRobot, self).ding()
        response = ear.listen()
        print 'response: ' + response
        ws.close()

    def token(self):
        serviceName = 'speech-to-text'
        uri = self.hostname +  "/authorization/api/v1/token?url=" + self.hostname + '/' + serviceName + "/api"
        uri = uri.replace("wss://", "https://");
        uri = uri.replace("ws://", "https://");
        resp = requests.get(uri, auth=(self.username, self.password),
                          verify=False, 
                          headers= {'Accept': 'application/json'},
                          timeout= (30, 30))

        jsonObject = resp.json()
        return jsonObject['token']

