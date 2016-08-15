from mouth import GoogleMouth
from body import ApiBody

"""
alfred
~~~~~~~~~~~~~~~~
Main module to launch the application.
"""

def main():
    print("Load actions")
    print("Load mouth")
    mouth = GoogleMouth()

    print("Load head");
    body = ApiBody(mouth)
    body.waitForRequest()

if __name__ == '__main__':
    main()
