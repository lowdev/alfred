from .stt import ApiRobot
from .stt import BingRobot

class RobotFactory:
    @staticmethod
    def produce(config, speaker, actions):
        configSTT = config['stt']
        if configSTT == 'bing':
           return BingRobot(config['bing'], speaker, actions)

        return ApiRobot(config['apiai'], speaker, actions)
