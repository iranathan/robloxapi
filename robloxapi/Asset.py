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
    

            
            
        
