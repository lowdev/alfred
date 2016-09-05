from ..robot import Robot

import requests

from websocket import create_connection
from base64 import b64encode

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

    def listen(self):
        token = self.token()

        ws = create_connection(self.url + '&watson-token=' + token)
        ws.send("{\"action\": \"start\", \"content-type\": \"audio/l16;rate=22050\"}")
        result =  ws.recv()
        print "Received '%s'" % result
        ws.close()
