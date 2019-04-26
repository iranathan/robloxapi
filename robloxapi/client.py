from .User import User
from .Group import Group
def client(cookie=str()):
    global functions
    functions = lambda: None
    functions.User = User(cookie, False)
    functions.Group = Group(cookie, False)
    return functions
       
