import json
class Trade:

    def __init__(self, request):
        self._request = request.request
        self.authorized = request.auth
        self.getTrades = 'https://www.roblox.com/my/money.aspx/getmyitemtrades'
        self.action = 'https://www.roblox.com/trade/tradehandler.ashx'

    def getTradeList(self):
        data = {
            'startindex': 0,
            'statustype': 'inbound'
        }
        r = self._request(url=self.getTrades, data=json.dumps(data), method='POST')
        return json.loads(r)['d']
    
    def getTrade(tradeId):
        data = {
            'TradeID': tradeId,
            'cmd': 'pull'
        }
        r = self._request(url=self.action, data=json.dumps(data), method='POST')
        return json.loads(r)
        

    def acceptTrade(tradeId):
        data = {
            'TradeID': tradeId,
            'cmd': 'accept'
        }
        r = self._request(url=self.action, data=json.dumps(data), method='POST')
        return json.loads(r)
    
    def declineTrade(tradeId):
        data = {
            'TradeID': tradeId,
            'cmd': 'decline'
        }
        r = self._request(url=self.action, data=json.dumps(data), method='POST')
        return json.loads(r)
