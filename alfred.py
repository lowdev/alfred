from mouth import GoogleMouth
from body import ApiBody
import yaml

"""
alfred
~~~~~~~~~~~~~~~~
Main module to launch the application.
"""

def main():
    print("Load config")
    
    config = None
    try:
        with open('profile.yml', "r") as f:
            config = yaml.safe_load(f)
    except OSError:      
        raise

    print("Load actions")
    print("Load mouth")
    mouth = GoogleMouth()

    print("Load head");
    body = ApiBody(config['apiai'], mouth)
    body.waitForRequest()

if __name__ == '__main__':
    main()
