class Requester(object):
    def __init__(self, requester):
        raise NotImplementedError("this is an abstract class")

    def send(self, data):
        raise NotImplementedError("this is an abstract class")

    def getResponse(self):
        raise NotImplementedError("this is an abstract class")
