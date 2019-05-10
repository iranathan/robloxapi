import json
class Asset:
    def __init__(self, request):
        self._request = request.request
    
    def getOutfits(self):
        url = 'https://avatar.roblox.com/v1/recent-items/all/list'
        r = self._request(url=url, method='GET')
        data = json.loads(r)
        Outfits = {}
        for item in data['data']:
            print(item)
