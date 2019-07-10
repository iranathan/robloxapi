import requests
class Auth:
    def __init__(self, request, client):
        self._request = request.request
        self.client_class = client
        self.get = request.get_headers

    def login(self, cookie):
        url = 'https://www.roblox.com/game/GetCurrentUser.ashx'
        cookies = {
            '.ROBLOSECURITY': cookie
        }
        headers = self.get()
        r = requests.get(url, cookies=cookies, headers=headers)
        if r.text == 'null':
            return False
        else:
            return self.client_class(cookie)

    def RefreshToken(self):
        url = 'https://www.roblox.com/authentication/signoutfromallsessionsandreauthenticate'
        r = self._request(url=url, method='POST')
        return r.cookies

    def IsUsenameTaken(self, username):
        url = f'https://auth.roblox.com/v1/usernames/validate?birthday=9999-06-08T22:00:00.000Z&context=Signup&username={username}'
        r = self._request(url=url)
        if json.loads(r)['code'] == 0:
            return False
        else:
            return True