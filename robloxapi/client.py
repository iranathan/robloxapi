from .request import request
from .User import User
from .Group import Group
from .Trade import Trade
class client:
    def __init__(self, cookie):
        self.request_client = request(cookie)
        self.user_info = self.request_client.user_info
        self.Group = Group(self.request_client)
        self.User = User(self.request_client)
        self.Trade = Trade(self.request_client)
