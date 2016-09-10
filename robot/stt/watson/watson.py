from ...robot import Robot

from stt_watson.SttWatson import SttWatson
from stt_watson.SttWatsonLogListener import SttWatsonLogListener
from config.Config import Config
import os.path
import argparse
import pkgutil
import yaml

class WatsonRobot(Robot):
    def __init__(self, config, speaker, actions):
        super(WatsonRobot, self).__init__(config, speaker, actions)

    def name(self):
        return 'Watson'

    def listen(self):
        sttWatsonLogListener = SttWatsonLogListener()
        sttWatson = SttWatson(self.config)
        sttWatson.addListener(sttWatsonLogListener)
        sttWatson.run()
