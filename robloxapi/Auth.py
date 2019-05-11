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
        if r.text != 'null':
            return False
        else:
            return client(cookie)

