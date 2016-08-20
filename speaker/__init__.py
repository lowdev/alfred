from .speakerFactory import SpeakerFactory
from .speaker import Speaker
from .tts import GoogleSpeaker
from .tts import WatsonSpeaker

"""
alfred
~~~~~~~~~~~~~~~~
Library for performing with support for several engines and APIs, online and offline.
"""

__all__ = [
    'SpeakerFactory',
    'Speaker',
    'GoogleSpeaker',
    'WatsonSpeaker'
]
