import requests
from .User import User
from .Group import Group
def client(cookie=str()):
    global functions
        r = requests.get('https://www.roblox.com/game/GetCurrentUser.ashx', cookies=cookies)
            functions = lambda: None
            functions.User = User(cookie, False)
            functions.Group = Group(cookie, False)
            return functions
       
