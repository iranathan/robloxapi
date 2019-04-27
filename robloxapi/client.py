from .request import request
from .User import User
from .Group import Group
def client(cookie=str()):
    global functions
    functions = lambda: None
    functions.User = User(request(cookie))
    functions.Group = Group(request(cookie))
    return functions
        





