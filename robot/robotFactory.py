from .stt import ApiRobot
from .stt import BingRobot
from .stt import WatsonRobot
from .stt import WitaiRobot

class RobotFactory:
    @staticmethod
    def produce(config, speaker, actions):
        configSTT = config['stt']
        if configSTT == 'bing':
           return BingRobot(config['bing'], speaker, actions)

        if configSTT == 'watson':
           return WatsonRobot(config['watson-stt'], speaker, actions)

        if configSTT == 'witai':
           return WitaiRobot(config['witai-stt'], speaker, actions)

        return ApiRobot(config['apiai'], speaker, actions)
