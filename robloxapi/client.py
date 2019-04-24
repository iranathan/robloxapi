import requests
from .User import User
def client(cookie=str()):
    global functions
    if cookie:
        cookies = {
            '.ROBLOSECURITY': cookie
        }
        r = requests.get('https://www.roblox.com/game/GetCurrentUser.ashx', cookies=cookies)
        if r.text is 'null':
            print('Rython: Failed to login. Using Rython without login')
            functions = lambda: None
            functions.User = User()
            return functions
        else:   
            functions = lambda: None
            functions.User = User(cookie, r)
            return functions
    else:
        functions = lambda: None
        functions.User = User()
        return functions



