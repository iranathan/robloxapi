
class Trade:

    def __init__(self, request):
        self._request = request.request
        self.authorized = request.auth
        self.getTrades = 'https://www.roblox.com/my/money.aspx/getmyitemtrades'
        self.action = 'https://www.roblox.com/trade/tradehandler.ashx'

    def getTradeList(self):
        r = self._request(url=self.getTrades, method='GET')
        return r

    def acceptTrade(tradeId):
        data = {
            'TradeID': tradeId,
            'cmd': 'accept'
        }
        r = self._request(url=self.action, method='GET')
        return r
    
    def declineTrade(tradeId):
        data = {
            'TradeID': tradeId,
            'cmd': 'decline'
        }
        r = self._request(url=self.action, method='GET')
        return r
