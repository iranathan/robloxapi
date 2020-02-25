import json
from .user import *


class TradeRequest:
    def __init__(self, request, date, expires, trade_partner_name, trade_partner_id, status, trade_id):
        self.request = request
        self.date = date
        self.expires = expires
        self.trade_partner = User(self.request, trade_partner_id, trade_partner_name)
        self.status = status,
        self.trade_id = trade_id

    async def send_cmd(self, cmd):
        data = {
            'TradeID': self.trade_id,
            'cmd': cmd
        }
        return await self.request.request(url='https://www.roblox.com/trade/tradehandler.ashx', method='POST', data=data)

    async def accept(self) -> int:
        r = await self.send_cmd('accept')
        return r.status_code

    async def decline(self) -> int:
        r = await self.send_cmd('decline')
        return r.status_code
