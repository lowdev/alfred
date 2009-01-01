from speaker import GoogleSpeaker
from speaker import WatsonSpeaker
from robot import ApiRobot
import yaml

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
    print("Load speaker")
    speaker = WatsonSpeaker(config['watson'])

    print("Load head");
    robot = ApiRobot(config['apiai'], speaker)
    robot.waitForRequest()

if __name__ == '__main__':
    main()
