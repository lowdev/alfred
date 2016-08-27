from ..robot import Robot

import speech_recognition as sr

class BingRobot(Robot):
    def __init__(self, config, speaker, actions):
        super(BingRobot, self).__init__(config, speaker, actions)
        self.BING_KEY = config['key']

    def name(self):
        return 'Bing'

    def listen(self):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source)
            print("Say something!")
            super(BingRobot, self).ding()
            audio = r.listen(source, 5)

        text = ''
        try:
            text = r.recognize_bing(audio, self.BING_KEY)
        except:
            print "I don't understand..."
        
        print 'text: ' + text
        return (None, text)
