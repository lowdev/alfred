from mouth import GoogleMouth

"""
alfred
~~~~~~~~~~~~~~~~
Main module to launch the application.
"""

def main():
    print("Load actions")
    print("Load mouth")
    mouth = GoogleMouth()
    mouth.speak("Hello")
    print("Load head");

if __name__ == '__main__':
    main()
