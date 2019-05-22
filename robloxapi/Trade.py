import json
from utils.JSON import is_num


class Trade:

    def __init__(self, request):
        self._request = request.request
        self.authorized = request.auth
        self.getTrades = 'https://www.roblox.com/my/money.aspx/getmyitemtrades'
        self.action = 'https://www.roblox.com/trade/tradehandler.ashx'
        self.Id = request.user_info['Id']
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
        return json.loads(r)['d']

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
        url = f'https://inventory.roblox.com/v1/users/{self.Id}/assets/collectibles?cursor=&sortOrder=Desc&limit=100'
        r = self._request(url=url)
        data = json.loads(r)
        TradeJSON = {}
        TradeJSON['AgentOfferList'] = [{
            'AgentOfferList': [],
            'IsActive': False,
            'TradeStatus': 'Open'
        }]
        tradeMe = {
            'AgentID': self.Id,
            'OfferList': [],
            'OfferRobux': 0,
            'OfferValue': 0
        }
        for item in data:
            if item in SendItems:
                assetId = item['assetId']
                tradeMe['OfferList'].append({
                    'UserAssetID': item['userAssetId'],
                    'Name': item['name'].replace(' ', '+'),
                    'ItemLink': f'https://www.roblox.com/catalog/{assetId}/redirect',
                    'ImageLink': f'https://www.roblox.com/asset-thumbnail/image?assetId={assetId}&height=110&width=110',
                    'AveragePrice': item['recentAveragePrice'],
                    'OriginalPrice': item['originalPrice'],
                    'SerialNumber': item['serialNumber'],
                    'SerialNumberTotal': item['assetStock'],
                    'MembershipLevel': item['buildersClubMembershipType']
                })
                tradeMe['OfferValue'] = tradeMe['OfferValue'] + int(item['recentAveragePrice'])
        TradeJSON['AgentOfferList'].append(tradeMe)
        #
        # check for items to get from trade
        #
        url = f'https://inventory.roblox.com/v1/users/{id}/assets/collectibles?cursor=&sortOrder=Desc&limit=100'
        userItems = self._request(url=url, method='GET')
        for item in userItems:
            if item in GetItems:
                tradeMe = self.tradeFormat
                tradeMe['AgentID'] = id
                assetId = item['assetId']
                tradeMe['OfferList'].append({
                    'UserAssetID': item['userAssetId'],
                    'Name': item['name'].replace(' ', '+'),
                    'ItemLink': f'https://www.roblox.com/catalog/{assetId}/redirect',
                    'ImageLink': f'https://www.roblox.com/asset-thumbnail/image?assetId={assetId}&height=110&width=110',
                    'AveragePrice': item['recentAveragePrice'],
                    'OriginalPrice': item['originalPrice'],
                    'SerialNumber': item['serialNumber'],
                    'SerialNumberTotal': item['assetStock'],
                    'MembershipLevel': item['buildersClubMembershipType']
                })
                tradeMe['OfferValue'] = tradeMe['OfferValue'] + int(item['recentAveragePrice'])
        TradeJSON['AgentOfferList'].append(tradeMe)

        return TradeJSON

    # https://inventory.roblox.com/v1/users/109503558/assets/collectibles?cursor=&sortOrder=Desc&limit=25

    """
    TradeJSON = {"AgentOfferList": [{"AgentID": 109503558, "OfferList": [
        {"UserAssetID": "12515090617", "Name": "Portrait+of+a+Hero+Camping",
         "ItemLink": "https://www.roblox.com/catalog/904541305/Portrait-of-a-Hero-Camping",
         "ImageLink": "https://www.roblox.com/asset-thumbnail/image?assetId=904541305&height=110&width=110",
         "AveragePrice": 1758, "OriginalPrice": "---", "SerialNumber": 288, "SerialNumberTotal": 569,
         "MembershipLevel": null}], "OfferRobux": 0, "OfferValue": 1758}, {"AgentID": 286018909, "OfferList": [
        {"UserAssetID": "3126016213", "Name": "Portrait+of+a+Hero+in+ROBLOX+",
         "ItemLink": "https://www.roblox.com/catalog/331486631/Portrait-of-a-Hero-in-ROBLOX",
         "ImageLink": "https://www.roblox.com/asset-thumbnail/image?assetId=331486631&height=110&width=110",
         "AveragePrice": 831, "OriginalPrice": "---", "SerialNumber": "---", "SerialNumberTotal": "---",
         "MembershipLevel": null}], "OfferRobux": 0, "OfferValue": 831}], "IsActive": false, "TradeStatus": "Open"}
         """

