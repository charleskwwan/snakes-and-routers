import requests # python-requests.org

TRACKER = "https://snakes-and-routers.herokuapp.com" # change to heroku later
FIND_GAME = "/findgame"
ADD_GAME = "/addgame"
REMOVE_GAME = "/removegame"

class RequestException(Exception):
    pass

# todo: implement more branches, other than always raise RequestException
def findGame():
    try:
        r = requests.get(TRACKER + FIND_GAME)
        hostaddr = r.json()["host"]
        if hostaddr:
            return tuple(hostaddr)
        else:
            raise RequestException
    except requests.exceptions.RequestException:
        raise RequestException
    except ValueError: # somehow, server doesnt send back json
        raise RequestException

def addGame():
    try:
        r = requests.post(TRACKER + ADD_GAME, data={})
        addr = r.json()["addr"]
        return tuple(addr)
    except requests.exceptions.RequestException:
        raise RequestException
    except ValueError: # somehow, server doesnt send back json
        raise RequestException

def removeGame(addr):
    try:
        payload = {"host": addr}
        r = requests.post(TRACKER + REMOVE_GAME, json=payload)
    except requests.exceptions.RequestException:
        raise RequestException
