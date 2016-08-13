class Body(object):
    """Abstract body class."""
    def __init__(self, mouth):
        raise NotImplementedError("this is an abstract class")

    def waitForRequest(self):
        raise NotImplementedError("this is an abstract class")
