#copyright (C) 2015 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Sample that streams audio to the Google Cloud Speech API via GRPC."""

from __future__ import division

import contextlib
import re
import signal
import threading

from google.cloud.speech.v1beta1 import cloud_speech_pb2 as cloud_speech
from google.cloud import credentials
from google.rpc import code_pb2
from grpc.beta import implementations
from grpc.framework.interfaces.face import face
import pyaudio
from six.moves import queue

import os
from ...snowboy import snowboydetect
from ..vad import ApiaiVAD
try:
    import apiai 
except ImportError:
    sys.path.append(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir)
    )
    import apiai

TOP_DIR = os.path.dirname(os.path.abspath(__file__))
RESOURCE_FILE = os.path.join(TOP_DIR, "../../snowboy/resources/common.res")
MODEL_FILE = os.path.join(TOP_DIR, "../../snowboy/model.pmdl")

class TranscribeStreaming(object):
    # Audio recording parameters
    RATE = 16000
    CHUNK = int(RATE / 10)  # 100ms

    # The Speech API has a streaming limit of 20 seconds of audio*, so keep the
    # connection alive for that long, plus some more to give the API time to figure
    # out the transcription.
    # * https://g.co/cloud/speech/limits#content
    DEADLINE_SECS = 20 * 3 + 5
    SPEECH_SCOPE = 'https://www.googleapis.com/auth/cloud-platform'

    def __init__(self):
        self.detector = snowboydetect.SnowboyDetect(
            resource_filename=RESOURCE_FILE.encode(),
            model_str=MODEL_FILE.encode())
        self.detector.SetAudioGain(1)
        self.resampler = apiai.Resampler(source_samplerate=self.RATE)
        self.vad = ApiaiVAD()

    def make_channel(self, host, port):
        """Creates an SSL channel with auth credentials from the environment."""
        # In order to make an https call, use an ssl channel with defaults
        ssl_channel = implementations.ssl_channel_credentials(None, None, None)

        # Grab application default credentials from the environment
        creds = credentials.get_credentials().create_scoped([self.SPEECH_SCOPE])
        # Add a plugin to inject the creds into the header
        auth_header = (
            'Authorization',
            'Bearer ' + creds.get_access_token().access_token)
        auth_plugin = implementations.metadata_call_credentials(
            lambda _, cb: cb([auth_header], None),
            name='google_creds')

        # compose the two together for both ssl and google auth
        composite_channel = implementations.composite_channel_credentials(
            ssl_channel, auth_plugin)

        return implementations.secure_channel(host, port, composite_channel)


    def _audio_data_generator(self, buff):
        """A generator that yields all available data in the given buffer.
        Args:
            buff - a Queue object, where each element is a chunk of data.
        Yields:
            A chunk of data that is the aggregate of all chunks of data in `buff`.
            The function will block until at least one data chunk is available.
        """
        while True:
            # Use a blocking get() to ensure there's at least one chunk of data
            chunk = buff.get()
            #frames, data = self.resampler.resample(chunk, 1)
            #state = self.vad.processFrame(frames)
            state = self.detector.RunDetection(chunk)
            print "state : " + str(state)
            if not chunk:
                # A falsey value indicates the stream is closed.
                break
            data = [chunk]

            # Now consume whatever other data's still buffered.
            while True:
                try:
                    data.append(buff.get(block=False))
                except queue.Empty:
                    break

            yield b''.join(data)

    def _processChunk(self, chunk):
        print "test"

    def _fill_buffer(self, audio_stream, buff, chunk):
        """Continuously collect data from the audio stream, into the buffer."""
        try:
            while True:
                buff.put(audio_stream.read(chunk))
        except IOError:
            # This happens when the stream is closed. Signal that we're done.
            buff.put(None)


    # [START audio_stream]
    @contextlib.contextmanager
    def record_audio(self, rate, chunk):
        """Opens a recording stream in a context manager."""
        audio_interface = pyaudio.PyAudio()
        audio_stream = audio_interface.open(
            format=pyaudio.paInt16,
            # The API currently only supports 1-channel (mono) audio
            # https://goo.gl/z757pE
            channels=1, rate=self.detector.SampleRate(),
            input=True, frames_per_buffer=chunk,
        )

        # Create a thread-safe buffer of audio data
        buff = queue.Queue()

        # Spin up a separate thread to buffer audio data from the microphone
        # This is necessary so that the input device's buffer doesn't overflow
        # while the calling thread makes network requests, etc.
        fill_buffer_thread = threading.Thread(
            target=self._fill_buffer, args=(audio_stream, buff, chunk))
        fill_buffer_thread.start()

        yield self._audio_data_generator(buff)

        audio_stream.stop_stream()
        audio_stream.close()
        fill_buffer_thread.join()
        audio_interface.terminate()
    # [END audio_stream]


    def request_stream(self, data_stream, rate):
        """Yields `StreamingRecognizeRequest`s constructed from a recording audio
        stream.
        Args:
            data_stream: A generator that yields raw audio data to send.
            rate: The sampling rate in hertz.
        """
        # The initial request must contain metadata about the stream, so the
        # server knows how to interpret it.
        recognition_config = cloud_speech.RecognitionConfig(
            # There are a bunch of config options you can specify. See
            # https://goo.gl/KPZn97 for the full list.
            encoding='LINEAR16',  # raw 16-bit signed LE samples
            sample_rate=rate,  # the rate in hertz
            # See
            # https://g.co/cloud/speech/docs/best-practices#language_support
            # for a list of supported languages.
            language_code='en-US',  # a BCP-47 language tag
        )
        streaming_config = cloud_speech.StreamingRecognitionConfig(
            config=recognition_config,
        )

        yield cloud_speech.StreamingRecognizeRequest(
            streaming_config=streaming_config)

        for data in data_stream:
            # Subsequent requests can all just have the content
            yield cloud_speech.StreamingRecognizeRequest(audio_content=data)


    def listen_print_loop(self, recognize_stream):
        for resp in recognize_stream:
            if resp.error.code != code_pb2.OK:
                raise RuntimeError('Server error: ' + resp.error.message)

            recognized_sentence = None
            # Display the transcriptions & their alternatives
            for result in resp.results:
                print result.alternatives
                recognized_sentence = result.alternatives

            if recognized_sentence:
                return recognized_sentence

            # Exit recognition if any of the transcribed phrases could be
            # one of our keywords.
            if any(re.search(r'\b(exit|quit)\b', alt.transcript, re.I)
                   for result in resp.results
                   for alt in result.alternatives):
                print('Exiting..')
                break

    def listen(self, onReady):
        with cloud_speech.beta_create_Speech_stub(
                self.make_channel('speech.googleapis.com', 443)) as service:
            # For streaming audio from the microphone, there are three threads.
            # First, a thread that collects audio data as it comes in
            with self.record_audio(self.RATE, self.CHUNK) as buffered_audio_data:
                onReady()
                print "Ready"
                # Second, a thread that sends requests with that data
                requests = self.request_stream(buffered_audio_data, self.RATE)
                # Third, a thread that listens for transcription response
                recognize_stream = service.StreamingRecognize(
                    requests, self.DEADLINE_SECS)

                # Exit things cleanly on interrupt
                signal.signal(signal.SIGINT, lambda *_: recognize_stream.cancel())

                # Now, put the transcription responses to use.
                try:
                    result = self.listen_print_loop(recognize_stream)
                    recognize_stream.cancel()
                    return result[0].transcript

                except face.CancellationError:
                    # This happens because of the interrupt handler
                    pass

