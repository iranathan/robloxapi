import http3, logging, asyncio, requests
from .errors import *


class Request:
    def __init__(self, cookie=None):
        self.requests = http3.AsyncClient()
        self.cookies = {}
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:66.0) Gecko/20100101 Firefox/66.0',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.5',
            'Content-Type': 'application/json;charset=utf-8',
            'Origin': 'https://www.roblox.com',
            'X-CSRF-TOKEN': '',
            'DNT': '1',
        }
        if cookie:
            self.login(cookie)

    async def xcsrf(self):
        r = await self.requests.post('https://www.roblox.com/favorite/toggle')
        if r.headers['X-CSRF-TOKEN']:
            return r.headers['X-CSRF-TOKEN']
        else:
            return None

    async def request(self, **kwargs):
        if not 'method' in kwargs: kwargs['method'] = 'GET'
        if kwargs['method'] == "POST" and not '.ROBLOSECURITY' in self.cookies:
            raise NotAuthenticated("You can't preform a post request without being authenticated.")
        r = await self.requests.request(kwargs['method'], kwargs['url'], headers=self.headers, cookies=self.cookies, data=kwargs.get('data'))
        if r.status_code == 403 and r.headers.get('X-CSRF-TOKEN'):
            self.headers['X-CSRF-TOKEN'] = r.headers.get('X-CSRF-TOKEN')
            return await self.request(**kwargs)
        elif not r.status_code == 200:
            if not kwargs.get('noerror'):
                raise BadStatus(f'Got status {r.status_code} from {kwargs["url"]} data: {r.text}')
        return r

    def check_parameter(self, provided, type_str):
        pass

    def login(self, cookie):
        cookies = {
            '.ROBLOSECURITY': cookie
        }
        r = requests.get('https://www.roblox.com/game/GetCurrentUser.ashx', cookies=cookies, headers=self.headers)
        if r.text != 'null':
            self.cookies = cookies
        else:
            raise NotAuthenticated("Cookie was incorrect.")

