from ..body import Body

class ApiBody(Body):
    def __init__(self, mouth):
        self.mouth = mouth

    def waitForRequest(self):
        print("I'm waiting")
   
