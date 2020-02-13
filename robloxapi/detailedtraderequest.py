from .utils.classes import Limited


class DetailedTradeRequest:
    def __init__(self, give: Limited, receive: Limited):
        self.give = give  # Items you will give
        self.receive = receive  # Items you will receive
