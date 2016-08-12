from ..mouth import Mouth 
from gtts import gTTS

class GoogleMouth(Mouth):
    def speak(self, sentence):
       print("say: " + sentence)
