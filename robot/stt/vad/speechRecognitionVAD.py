class SpeechRecognitionVAD(object):

    def __init__(self):
        """
        Creates a new ``VAD`` instance
        """
        self.energy_threshold = 300 # minimum audio energy to consider for recording
        self.dynamic_energy_threshold = True
        self.dynamic_energy_adjustment_damping = 0.15
        self.dynamic_energy_ratio = 1.5
        self.pause_threshold = 0.8 # seconds of non-speaking audio before a phrase is considered complete
        self.phrase_threshold = 0.3 # minimum seconds of speaking audio before we consider the speaking audio a phrase - values below this are ignored (for filtering out clicks and pops)
        self.non_speaking_duration = 0.5 # seconds of non-speaking audio to keep on both sides of the recording

        self.phrase_count = 0
        self.pause_count = 0
        self.pause_buffer_count = 0
        self.end_of_phrase = False
        self.phrase_buffer_count = 0

    def adjust_for_ambient_noise(self, source, duration = 1):
        """
        Adjusts the energy threshold dynamically using audio from ``source`` (an ``AudioSource`` instance) to account for ambient noise.
        Intended to calibrate the energy threshold with the ambient energy level. Should be used on periods of audio without speech - will stop early if any speech is detected.
        The ``duration`` parameter is the maximum number of seconds that it will dynamically adjust the threshold for before returning. This value should be at least 0.5 in order to get a representative sample of the ambient noise.
        """
        assert isinstance(source, AudioSource), "Source must be an audio source"
        assert source.stream is not None, "Audio source must be entered before adjusting, see documentation for `AudioSource`; are you using `source` outside of a `with` statement?"
        assert self.pause_threshold >= self.non_speaking_duration >= 0

        seconds_per_buffer = (source.CHUNK + 0.0) / source.SAMPLE_RATE
        elapsed_time = 0

        # adjust energy threshold until a phrase starts
        while True:
            elapsed_time += seconds_per_buffer
            if elapsed_time > duration: break
            buffer = source.stream.read(source.CHUNK)
            energy = audioop.rms(buffer, source.SAMPLE_WIDTH) # energy of the audio signal

            # dynamically adjust the energy threshold using assymmetric weighted average
            damping = self.dynamic_energy_adjustment_damping ** seconds_per_buffer # account for different chunk sizes and rates
            target_energy = energy * self.dynamic_energy_ratio
            self.energy_threshold = self.energy_threshold * damping + target_energy * (1 - damping)


    def is_speech(buffer):
        self.phrase_count += 1
        energy = audioop.rms(buffer, source.SAMPLE_WIDTH) # energy of the audio signal
        if energy > self.energy_threshold:
            self.pause_count = 0
        else:
            self.pause_count += 1
        if self.pause_count > self.pause_buffer_count: # end of the phrase
            self.end_of_phrase = True

        if self.end_of_phrase:
            self.phrase_count -= self.pause_count # exclude the buffers for the pause before the phrase
            if self.phrase_count >= self.phrase_buffer_count or len(buffer) == 0:
                return 1 # phrase is long enough or we've reached the end of the stream, so stop listening

        return 0
