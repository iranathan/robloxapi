from bs4 import BeautifulSoup
class Game:
    def __init__(self, request):
        self._request = request.request


    def getGame(self, id):
        url = f'https://web.roblox.com/games/{id}/redirect'
        data = {}
        r = self._request(url=url, method='GET', allow_redirects=True)
        if r.status_code == '200':
            soup = BeautifulSoup(r.text, 'html.parser')
            found = soup.find('div', {'class': 'game-title-container'})
            data['title'] = found.h2['title']
            owner_type = ''
            if found.div.a['href'].startswith('https://web.roblox.com/groups/group.aspx?gid='):
                owner_type = 'group'
            elif found.div.a['href'].startswith('https://web.roblox.com/users/'):
                owner_type = 'user'
            data['owner'] = {
                'type': owner_type
                'name': found.div.a.text,
                'link': found.div.a['href']
            }
            vote_numbers = soup.find('div', {'class': 'vote-numbers'})

            data['votes'] = {
                'likes': vote_numbers.div.span['title'],
                'dislikes': vote_numbers.div.child.span['title']
            }
