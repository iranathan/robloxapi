import json
class Asset:
    def __init__(self, request):
        self._request = request.request
    
    def getOutfits(self):
        url = 'https://avatar.roblox.com/v1/users/109503558/outfits?isEditable=true&itemsPerPage=50&page=1'
        r = self._request(url=url, method='GET')
        data = json.loads(r)
        Outfits = {}
        for item in data['data']:
            url = 'https://www.roblox.com/outfit-thumbnail/json?width=150&height=150&format=png&userOutfitId=' + str(item['id'])
            outfit_data = json.loads(self._request(url=url, method='GET'))
            Outfits[item['name']] = {
                'id': item['id'],
                'image': outfit_data['Url']
            }
        return Outfits
    
    def wearOutfit(self, OutfitId):
        url = f'https://avatar.roblox.com/v1/outfits/{OutfitId}/wear'
        data = self._request(url=url, method='POST')
        return json.loads(data)

    def searchCatalog(self, keyword, page=1):
        keyword = str(keyword).replace(' ', '+')
        url = f'https://search.roblox.com/catalog/items?Category=1&Direction=2&Keyword={keyword}&PageNumber={page}'
        r = self._request(url=url, method='GET')
        return json.loads(r)['Items']

    def getAssetInfo(self, id):
        url = 'http://api.roblox.com/marketplace/productinfo?assetId=' + str(id)
        return json.loads(self._request(url=url))

    def buyAsset(self, id):
        info = self.getAssetInfo(id)
        if str(info) == '{}': return False
        productId = info['ProductId']
        price = info['PriceInRobux']
        id = info['Creator']['Id']
        url = f'https://www.roblox.com/api/item.ashx?rqtype=purchase&productID={productId}&expectedCurrency=1&expectedPrice={price}&expectedSellerID={id}&userAssetID='
        r = self._request(url=url, method='POST')
        return json.loads(r)



            
            
