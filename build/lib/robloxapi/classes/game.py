import json


class Game:

    def __init__(self, request, gameId):
        self.id = gameId
        self._request = request.request
        self.selfId = request.user_info['Id']

    #like=True/False
    def voteGame(self, like):
        url = f'https://www.roblox.com/voting/vote?assetId={self.id}&'
        if like is True:
            url += 'vote=true'
        else:
            url += 'vote=null'

        r = self._request(url=url, method='POST')
        data = json.loads(r)
        if not 'Success' in data: return {'Success': False}
        return {
            'Success': data['Success'],
            'Message': data['message'],
            'ErrorType': data['ModalType']
        }

    def favoriteGame(self):
        url = 'https://www.roblox.com/favorite/toggle'
        data = {
            'assetID': self.id
        }
        r = self._request(url=url, method='POST', data=json.dumps(data))
        data = json.loads(r)
        return data