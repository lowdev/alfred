from ..mouth import Mouth

import os
import tempfile

import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst as gst
from gi.repository import GObject
#GObject.threads_init()
gst.init(None)

from gtts import gTTS

class GoogleMouth(Mouth):
   def speak(self, sentence):
       print("say: " + sentence)
       tts = gTTS(text=sentence, lang='en')
       with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as f:
           tmpfile = f.name
       tts.save(tmpfile)
       try:
           self.__play(tmpfile)
       finally:
           os.remove(tmpfile)

   def __play(self, file):
       gst.init()
       mainloop = GObject.MainLoop()

       #setting up a single "playbin" element which handles every part of the playback by itself
       pl = gst.ElementFactory.make("playbin", "player")
       pl.set_property('uri', 'file://' + os.path.abspath(file))

       bus = pl.get_bus()
       bus.add_signal_watch()

       def quit(bus, message):
           mainloop.quit()

       bus.connect("message::eos", quit)
       bus.connect("message::error", quit)

       #running the playbin 
       pl.set_state(gst.State.PLAYING)

       print("start to play")
       try:
           mainloop.run()
       finally:
           pl.set_state(gst.State.NULL)
