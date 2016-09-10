from ...robot import Robot

from stt_watson.SttWatson import SttWatson
from stt_watson.SttWatsonLogListener import SttWatsonLogListener
from recording.Record import Record
from watson_client.Client import Client
from utils.SignalHandler import SignalHandler

import threading
import signal
import os
import argparse
import pkgutil
import yaml

class WatsonRobot(Robot):
    def __init__(self, config, speaker, actions):
        super(WatsonRobot, self).__init__(config, speaker, actions)
        config['audio-chunk'] = 8000
        config['audio-rate'] = 44100
        config['channels'] = 1

        self.listeners = []
        sttWatsonLogListener = SttWatsonLogListener()
        self.listeners.append(sttWatsonLogListener)
        self.stopper = threading.Event()
        self.record = Record(config, self.stopper)
        self.workers = [self.record]
        self.watsonClient = Client(config)
        self.handler = SignalHandler(self.stopper, self.workers)
        signal.signal(signal.SIGINT, self.handler)

    def name(self):
        return 'Watson'

    def listen(self):
        audioFd, writer = os.pipe()
        self.record.setWriter(writer)
        self.record.start()
        self.watsonClient.setListeners(self.listeners)
        self.watsonClient.startStt(audioFd)

        sttWatson = SttWatson(self.config)
        sttWatson.addListener(sttWatsonLogListener)
        sttWatson.run()
