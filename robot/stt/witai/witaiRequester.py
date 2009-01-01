import json

class WitaiRequester(object):
    def __init__(self, requester):
        self.requester = requester
    
    def send(self, data):
        self.requester.send(data)
    
    def getResponse(self):
        print ("Wait for response...")
        httpResponse = self.requester.getresponse()
        #print 'Status : ' + httpResponse.status
        return json.loads(httpResponse.read())
