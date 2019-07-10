from bs4 import BeautifulSoup
import re



class Game:

    def __init__(self, request):
        self._request = request.request

    def searchGames(self, keyword):
        url = f'https://www.roblox.com/games/moreresultscached?StartRows=0&MaxRows=40&IsUserLoggedIn=true&NumberOfColumns=14&IsInHorizontalScrollMode=false&DeviceTypeId=1&Keyword={keyword}&AdSpan=98&AdAlignment=0&v=2&IsSecure=&UseFakeResults=False&SuggestedCorrection=none&SuggestionKeyword=&SuggestionReplacedKeyword=&QueryType=Bucketboost'
        r = self._request(url=url)
        soup = BeautifulSoup(r, 'html.parser')
        links = [item for item in soup.find_all('a', {'class': 'game-card-link'})]
        gameDict = {}
        for item in links:
            id = re.findall(r'\b\d+\b', item.get('href'))[2]
            if 'div' in item.div:
                name = item.div.div.img['alt']
                link = item['src']
            else:
                name = item.div.img['alt']
                link = item.div.img['src']
            gameDict[name] = {
                'name': name,
                'id': id,
                'link': link
            }
        return gameDict
    
    def favoritGame(gameId):
        url = 'https://www.roblox.com/favorite/toggle'
        data = json.dumps({
            'assetID': gameId
        })
        return json.loads(self._request(url=url, data=data))

    def getGameServers(self, id):
        url = f'https://www.roblox.com/games/getgameinstancesjson?placeId={id}&startIndex=0'
        r = self._request(url=url, method='GET')
        return json.loads(r)['Collection']




