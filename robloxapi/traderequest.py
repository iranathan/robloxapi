class TradeRequest:
    def __init__(self, request, date, expires, trade_partner_name, trade_partner_id, status, trade_id):
        self.request = request
        self.date = date
        self.expires = expires
        self.trade_partner = {
            'name': trade_partner_name,
            'id': trade_partner_id
        }
        self.status = status,
        self.trade_id = trade_id

    # TODO: Add get_trade function (there is a lot of json it returns thanks roblox)
    async def accept(self) -> int:
        data = {
            'TradeID': self.trade_id,
            'cmd': 'accept'
        }
        r = await self.request.request(url='https://www.roblox.com/trade/tradehandler.ashx', method='POST')
        return r.status_code

    async def decline(self) -> int:
        data = {
            'TradeID': self.trade_id,
            'cmd': 'decline'
        }
        r = await self.request.request(url='https://www.roblox.com/trade/tradehandler.ashx', method='POST')
        return r.status_code
