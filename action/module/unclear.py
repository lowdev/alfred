from sys import maxint
import random

WORDS = []

PRIORITY = -(maxint + 1)


def handle(text):
    """
        Reports that the user has unclear or unusable input.
        Arguments:
        text -- user-input, typically transcribed speech
    """

    messages = ["I'm sorry, could you repeat that?",
                "My apologies, could you try saying that again?",
                "Say that again?", "I beg your pardon?"]

    return random.choice(messages)

def isValid(text):
    return True
