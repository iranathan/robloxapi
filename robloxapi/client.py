from .utils.request import request
from .utils.events import Event
from .User import User
from .Group import Group
from .Trade import Trade
from .Asset import Asset
from .Auth import Auth
from .Game import Game
from .Chat import Chat

class client:
    def __init__(self, cookie='', debug=False, ready_event=None):
        self.request_client = request(cookie, debug=debug, ready_event=ready_event)
        self.Group = Group(self.request_client)
        self.User = User(self.request_client)
        self.Trade = Trade(self.request_client)
        self.Asset = Asset(self.request_client)
        self.Auth = Auth(self.request_client, client)
        self.Game = Game(self.request_client) #TODO: Add more functions to Game class.
        self.Chat = Chat(self.request_client)


        #Info
        self.cookie = cookie

    def bind_event(self, eventName, eventCallback, args=None):
        return Event(self.request_client, eventName, eventCallback, args, self)


    

