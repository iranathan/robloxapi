from .utils.request import *
from .user import *
from .group import *

class client:
    def __init__(self, cookie=None):
        self.request = Request(cookie)
        self.User = User(self.request)
        self.Group = Group(self.request)
