from utils.request import *
import user

class client:
    def __init__(self, cookie=None):
        self.request = Request(cookie)
        self.User = user.User(self.request)