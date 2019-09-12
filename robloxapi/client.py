from .utils.request import *
import user
import group

class client:
    def __init__(self, cookie=None):
        self.request = Request(cookie)
        self.User = user.User(self.request)
        self.Group = group.Group(self.request)
