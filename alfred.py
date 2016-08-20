from speaker import SpeakerFactory
from robot import ApiRobot
import yaml
import ssl
_create_unverified_https_context = ssl._create_unverified_context
ssl._create_default_https_context = _create_unverified_https_context

import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

"""
alfred
~~~~~~~~~~~~~~~~
Main module to launch the application.
"""

def getConfig():
    try:
        with open('profile.yml', "r") as f:
           return yaml.safe_load(f)
    except OSError:
        raise


def main():
    print("Load config")
    config = getConfig()

    print("Load actions")
    speaker = SpeakerFactory.produce(config)
    print(speaker.name() + " speaker is loaded")

    print("Load head")
    robot = ApiRobot(config['apiai'], speaker)
    robot.waitForRequest()

if __name__ == '__main__':
    main()
