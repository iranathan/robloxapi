from .utils.request import request
from .User import User
from .Group import Group
from .Trade import Trade
from .Asset import Asset
from .Auth import Auth
class client:
    def __init__(self, cookie=''):
        self.request_client = request(cookie)
        self.Group = Group(self.request_client)
        self.User = User(self.request_client)

    

