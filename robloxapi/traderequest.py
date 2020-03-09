import json
from .user import *
from .detailedtrade import DetailedTrade


class TradeRequest:
    """
    Represents a trade request.
    """
    def __init__(self, request, date, expires, trade_partner_name, trade_partner_id, status, trade_id):
        """
        Construct a new trade request class.
        :param request: Used to send requests
        :param date: The date of the trade
        :param expires: When the trade expires
        :param trade_partner_name: The roblox name of the partner
        :param trade_partner_id: The roblox id of the partner
        :param status: The trade status
        :param trade_id: The trade id
        """
        self.request = request
        self.date = date
        self.expires = expires
        self.trade_partner = User(self.request, trade_partner_id, trade_partner_name)
        self.status = status,
        self.trade_id = trade_id

    async def send_cmd(self, cmd):
        """
        Do something with the trade.
        :param cmd: What to do with the trade
        :return: Response
        """
        data = {
            'TradeID': self.trade_id,
            'cmd': cmd
        }
        return await self.request.request(url='https://www.roblox.com/trade/tradehandler.ashx', method='POST', data=data)

    async def get_detailed_trade(self) -> DetailedTrade:
        r = await self.send_cmd('pull')
        data = r.json()['data']
        data["AgentOfferList"]

    async def accept(self) -> int:
        """
        Accepts a trade.
        :return: StatusCode
        """
        r = await self.send_cmd('accept')
        return r.status_code

    async def decline(self) -> int:
        """
        Declines a trade request.
        :return: StatusCode
        """
        r = await self.send_cmd('decline')
        return r.status_code
