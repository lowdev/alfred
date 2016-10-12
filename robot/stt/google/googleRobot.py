from ...robot import Robot
from transcribeStreaming import TranscribeStreaming as Ear

import os

class GoogleRobot(Robot):
    def __init__(self, config, speaker, actions):
        super(GoogleRobot, self).__init__(config, speaker, actions)
        self.ear = Ear()
        self.__setEnvironementVariable(config['google_application_credentials'])

    def name(self):
        return 'Google'

    def listen(self):
        super(GoogleRobot, self).ding()
        response = self.ear.listen()

        print 'response: ' + str(response)
        return (None, response)

    def __setEnvironementVariable(self, value):
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = value