import os
import signal
from snowboy import snowboydecoder

TOP_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_FILE = os.path.join(TOP_DIR, "snowboy/model.pmdl")

class Robot(object):
    """Abstract robot class."""
    def __init__(self, config, speaker):
        self.speaker = speaker
        self.interrupted = False

    def speak(self, text):
        raise NotImplementedError("this is an abstract class")

    def listen(self):
        raise NotImplementedError("this is an abstract class")

    def startConversation(self):
        self.ding()
        response = self.listen()
        self.speak(response)

    def waitForRequest(self):
        signal.signal(signal.SIGINT, self.signal_handler)

        detector = snowboydecoder.HotwordDetector(MODEL_FILE, sensitivity=0.5)
        self.speak("What can i do for you ?")
        print('Listening... Press Ctrl+C to exit')

        # main loop
        detector.start(detected_callback=self.startConversation,
               interrupt_check=self.interrupt_callback,
               sleep_time=0.03)

        detector.terminate()

    def signal_handler(self, signal, frame):
        self.interrupted = True

    def interrupt_callback(self):
        return self.interrupted
