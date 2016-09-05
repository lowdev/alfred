from ..requester import Requester
import json

class ApiaiRequester(Requester):
    def __init__(self, requester):
        self.requester = requester
    
    def send(self, data):
        self.requester.send(data)
    
    def getResponse(self):
        print ("Wait for response...")
        httpResponse = self.requester.getresponse()
        return json.loads(httpResponse.read())
