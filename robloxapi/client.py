from .request import request
from .User import User
from .Group import Group
from .Trade import Trade
def client(cookie=str()):
    global functions
    functions = lambda: None
    functions.User = User(request(cookie))
    functions.Group = Group(request(cookie))
    functions.Trade = Trade(request(cookie))
    return functions
        





