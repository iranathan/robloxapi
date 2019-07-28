import json


class Trade:

    def __init__(self, request):
        self._request = request.request
        self.rawRequest = request
        self.authorized = request.auth
        self.getTrades = 'https://www.roblox.com/my/money.aspx/getmyitemtrades'
        self.action = 'https://www.roblox.com/trade/tradehandler.ashx'
        self.tradeFormat = {
            'AgentID': '',
            'OfferList': [],
            'OfferRobux': 0,
            'OfferValue': 0
        }

    def getTradeList(self):
        data = {
            'startindex': 0,
            'statustype': 'inbound'
        }
        r = self._request(url=self.getTrades, data=json.dumps(data), method='POST')
        return json.loads(json.loads(r)['d'])

    def getTrade(self, tradeId):
        data = {
            'TradeID': tradeId,
            'cmd': 'pull'
        }
        r = self._request(url=self.action, data=json.dumps(data), method='POST')
        return json.loads(r)

    def acceptTrade(self, tradeId):
        data = {
            'TradeID': tradeId,
            'cmd': 'accept'
        }
        r = self._request(url=self.action, data=json.dumps(data), method='POST')
        return json.loads(r)

    def declineTrade(self, tradeId):
        data = {
            'TradeID': tradeId,
            'cmd': 'decline'
        }
        r = self._request(url=self.action, data=json.dumps(data), method='POST')
        return json.loads(r)

    def sendTrade(self, id: int, SendItems: list, GetItems: list):
        selfId = self.rawRequest.user_info['Id']
        url = f'https://inventory.roblox.com/v1/users/{selfId}/assets/collectibles?cursor=&sortOrder=Desc&limit=100'
        r = self._request(url=url)
        data = json.loads(r)
        TradeJSON = {}
        TradeJSON['AgentOfferList'] = []
        tradeMe = {
            'AgentID': selfId,
            'OfferList': [],
            'OfferRobux': 0,
            'OfferValue': 0
        }
        for item in data['data']:
            if (len(list(filter(lambda x: str(x) == str(item['assetId']), SendItems))) > 0):
                assetId = item['assetId']
                tradeMe['OfferList'].append({
                    'UserAssetID': str(item['userAssetId']),
                    'Name': item['name'],
                    'ItemLink': f'https://www.roblox.com/catalog/{assetId}/redirect',
                    'ImageLink': f'https://www.roblox.com/asset-thumbnail/image?assetId={assetId}&height=110&width=110',
                    'AveragePrice': item['recentAveragePrice'],
                    'OriginalPrice': item['originalPrice'] or '---',
                    'SerialNumber': item['serialNumber'] or '---',
                    'SerialNumberTotal': item['assetStock'] or '---',
                    'MembershipLevel': item['buildersClubMembershipType'] if item['buildersClubMembershipType'] != 0 else None
                })
                tradeMe['OfferValue'] = tradeMe['OfferValue'] + int(item['recentAveragePrice'])
        TradeJSON['AgentOfferList'].append(tradeMe)
        #
        # check for items to get from trade
        #
        url = f'https://inventory.roblox.com/v1/users/{id}/assets/collectibles?cursor=&sortOrder=Desc&limit=100'
        userItems = self._request(url=url, method='GET')
        userItems = json.loads(userItems)
        tradeMe = self.tradeFormat
        for item in userItems['data']:
            if (len(list(filter(lambda x: str(x) == str(item['assetId']), GetItems))) > 0):
                tradeMe['AgentID'] = id
                assetId = item['assetId']
                tradeMe['OfferList'].append({
                    'UserAssetID': str(item['userAssetId']),
                    'Name': item['name'],
                    'ItemLink': f'https://www.roblox.com/catalog/{assetId}/redirect',
                    'ImageLink': f'https://www.roblox.com/asset-thumbnail/image?assetId={assetId}&height=110&width=110',
                    'AveragePrice': item['recentAveragePrice'],
                    'OriginalPrice': item['originalPrice'] or '---',
                    'SerialNumber': item['serialNumber'] or '---',
                    'SerialNumberTotal': item['assetStock'] or '---',
                    'MembershipLevel': item['buildersClubMembershipType'] if item['buildersClubMembershipType'] != 0 else None
                })
                tradeMe['OfferValue'] = tradeMe['OfferValue'] + int(item['recentAveragePrice'])
        TradeJSON['AgentOfferList'].append(tradeMe)
        TradeJSON['IsActive'] = False
        TradeJSON['TradeStatus'] = 'Open'
        #Send data to roblox

        data = {
            'cmd': 'send',
            'TradeJSON': json.dumps(TradeJSON).replace(' ', '')
        }
        r = self._request(url='https://www.roblox.com/Trade/tradehandler.ashx', data=data, method='POST', response=True)
        print(r.text)




