import requests
from src.User import User
def client(cookie=str()):
    global functions
    if cookie:
        cookies = {
            '.ROBLOSECURITY': cookie
        }
        r = requests.get('https://www.roblox.com/game/GetCurrentUser.ashx', cookies=cookies)
        if r is 'null':
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

rbx = client()
print(rbx.User.getProfile('109503558'))

   

