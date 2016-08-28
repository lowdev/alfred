import re
import json
import requests

WORDS = ["MEDIA", "BACK", "PLAY", "PAUSE", "STOP", "SELECT", "INFO", "UP", "DOWN", "START"]

def doJson(data, profile):
    kodi_ip = profile['kodi']['ip']
    kodi_port = profile['kodi']['port']
    kodi_username = profile['kodi']['user']
    kodi_password = profile['kodi']['password']

    xbmcUrl = "http://" + kodi_username + ":" + kodi_password + "@" + kodi_ip + ":" + str(kodi_port) + "/jsonrpc?request="
    data_json = json.dumps(data)
    r = requests.post(xbmcUrl, data_json)


def handle(text, profile):
    """
        Responds to user-input to control KODI.
        
        Current supports:
            -Pause / Play
            -Stop
            -Back
            -Up/Down/Left/Right
            -Info
            -Select
        Arguments:
        	text -- user-input, typically transcribed speech
       		mic -- used to interact with the user (for both input and output)
        	profile -- contains information related to the user (e.g., phone number)
    """

    textLowercase = text.lower()

    if 'pause' in textLowercase or 'play' in textLowercase:
        data = {'jsonrpc':'2.0','method':'Player.PlayPause','params':{'playerid':1},'id':1}
        doJson(data, profile)
    elif 'stop' in textLowercase:
        data = {'jsonrpc':'2.0','method':'Player.Stop','params':{'playerid':1},'id':1}
        doJson(data, profile)
    elif 'back' in textLowercase:
        data = {'jsonrpc':'2.0','method':'Input.Back','id':1}
        doJson(data, profile)
    elif 'select' in textLowercase:
        data = {'jsonrpc':'2.0','method':'Input.Select','id':1}
        doJson(data, profile)
    elif 'down' in textLowercase:
        data = {'jsonrpc':'2.0','method':'Input.Down','id':1}
        doJson(data, profile)
    elif 'up' in textLowercase:
        data = {'jsonrpc':'2.0','method':'Input.Up','id':1}
        doJson(data, profile)
    elif 'info' in textLowercase:
        data = {'jsonrpc':'2.0','method':'Input.Info','id':1}
        doJson(data, profile)
    else:
        return "Sorry I'm not aware of that KODI function yet"

def isValid(text):
    """
        Returns True if the text is related to xbmc.
        Arguments:
        	text -- user-input, typically transcribed speech
    """

    return 'tv' in text.lower()
