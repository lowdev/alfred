import os
import wave
import pyaudio
import time

TOP_DIR = os.path.dirname(os.path.abspath(__file__))
DETECT_DING = os.path.join(TOP_DIR, "resources/ding.wav")
DETECT_DONG = os.path.join(TOP_DIR, "resources/dong.wav")

class Speaker(object):
    """Abstract speaker class."""
    def speak(self, config):
        raise NotImplementedError("this is an abstract class")

    def ding(self):
        self.__playWave()        

    def dong(self):
        self.__playWave()

    def __playWave(self, fname):
        """Simple callback function to play a wave file.
        :param str fname: wave file name
        :return: None
        """
        ding_wav = wave.open(fname, 'rb')
        ding_data = ding_wav.readframes(ding_wav.getnframes())
        audio = pyaudio.PyAudio()
        stream_out = audio.open(
            format=audio.get_format_from_width(ding_wav.getsampwidth()),
            channels=ding_wav.getnchannels(),
            rate=ding_wav.getframerate(), input=False, output=True)
        stream_out.start_stream()
        stream_out.write(ding_data)
        time.sleep(0.2)
        stream_out.stop_stream()
        stream_out.close()
        audio.terminate()
