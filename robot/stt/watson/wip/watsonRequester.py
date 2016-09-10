from ..requester import Requester

class WatsonRequester(Requester):
    def __init__(self, requester):
        self.requester = requester
    
    def send(self, data):
        self.requester.send(data)
    
    def getResponse(self):
        self.requester.send('{"action": "stop"}')
        print ("Wait for response...")
        return self.requester.recv()
