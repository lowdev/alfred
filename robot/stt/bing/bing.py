from ...robot import Robot
from ..vad import ApiaiVAD

try:
    import apiai 
except ImportError:
    sys.path.append(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir)
    )
    import apiai

import speech_recognition as sr

import io

class BingRobot(Robot):
    def __init__(self, config, speaker, actions):
        super(BingRobot, self).__init__(config, speaker, actions)
        self.BING_KEY = config['key']
        self.vad = ApiaiVAD()
        self.resampler = apiai.Resampler(source_samplerate=16000)

    def name(self):
        return 'Bing'

    def listen(self):
        self.vad.reset()
        self.vad = ApiaiVAD()
        
        print("Say something!")
        super(BingRobot, self).ding()
        with sr.Microphone() as source:
            r = sr.Recognizer()
            audio = self.record(source, 5)

        text = ''
        try:
            text = r.recognize_bing(audio, self.BING_KEY)
        except:
            print "I don't understand..."
        
        print 'text: ' + text
        return (None, text)

    def record(self, source, duration = None, offset = None):
        """
        Records up to ``duration`` seconds of audio from ``source`` (an ``AudioSource`` instance) starting at ``offset`` (or at the beginning if not specified) into an ``AudioData`` instance, which it returns.
        If ``duration`` is not specified, then it will record until there is no more audio input.
        """
        assert isinstance(source, sr.AudioSource), "Source must be an audio source"
        assert source.stream is not None, "Audio source must be entered before recording, see documentation for `AudioSource`; are you using `source` outside of a `with` statement?"

        frames = io.BytesIO()
        seconds_per_buffer = (source.CHUNK + 0.0) / source.SAMPLE_RATE
        elapsed_time = 0
        offset_time = 0
        offset_reached = False
        frame_count = 0
        while True: # loop for the total number of chunks needed
            if offset and not offset_reached:
                offset_time += seconds_per_buffer
                if offset_time > offset:
                    offset_reached = True

            buffer = source.stream.read(source.CHUNK)
            frames2, data = self.resampler.resample(buffer, frame_count)
            state = self.vad.processFrame(frames2)
            print 'state: ' + str(state) + ', count: ' + str(frame_count)
            if state == 0: break
            if len(buffer) == 0: break

            if offset_reached or not offset:
                elapsed_time += seconds_per_buffer
                if duration and elapsed_time > duration: break

                frames.write(buffer)
            frame_count += 1

        frame_data = frames.getvalue()
        frames.close()
        return sr.AudioData(frame_data, source.SAMPLE_RATE, source.SAMPLE_WIDTH)
