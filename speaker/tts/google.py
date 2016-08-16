from ..speaker import Speaker

import os
import tempfile
import mad
import wave
import pyaudio
import subprocess

from gtts import gTTS

class GoogleSpeaker(Speaker):
   def speak(self, sentence):
       if not sentence:
           return
       
       print("say: " + sentence)
       tts = gTTS(text=sentence, lang='en')
       with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as f:
           tmpfile = f.name
       
       tts.save(tmpfile)
       try:
           self.__playMp3(tmpfile)
       finally:
           os.remove(tmpfile)
         
   def __playMp3(self, filename):
       mf = mad.MadFile(filename)
       with tempfile.NamedTemporaryFile(suffix='.wav') as f:
           wav = wave.open(f, mode='wb')
           wav.setframerate(mf.samplerate())
           wav.setnchannels(1 if mf.mode() == mad.MODE_SINGLE_CHANNEL else 2)
           # 4L is the sample width of 32 bit audio
           wav.setsampwidth(4L)
           frame = mf.read()
           while frame is not None:
               wav.writeframes(frame)
               frame = mf.read()
           wav.close()
           self.__playWav(f.name)
   
   def __playWav(self, filename):
       cmd = ['aplay', str(filename)]

       with tempfile.TemporaryFile() as f:
           subprocess.call(cmd, stdout=f, stderr=f)
           f.seek(0)
           output = f.read()
