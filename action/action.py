
class Action(object):

    def __init__(self):
       raise NotImplementedError("this is an abstract class")

    def keywords(self):
       raise NotImplementedError("this is an abstract class")

    def execute(self):
       raise NotImplementedError("this is an abstract class")
