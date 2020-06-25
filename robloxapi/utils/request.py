import http3, logging, asyncio, requests
from .errors import *


class Request:
    """
    Request class.
    """
    def __init__(self, cookie=None, debug=False):
        """
        Request class.
        :param cookie:
        """
        self.requests = http3.AsyncClient()
        self.debug = debug
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
        """
        Gets an xcstf token.
        :return: An xcsrf
        """
        r = await self.requests.post('https://www.roblox.com/favorite/toggle')
        if r.headers['X-CSRF-TOKEN']:
            return r.headers['X-CSRF-TOKEN']
        else:
            return None

    async def request(self, **kwargs):
        """
        Sends a request.
        :param kwargs: Options for the request
        :return: Response class
        """
        if not 'method' in kwargs: kwargs['method'] = 'GET'
        if kwargs['method'].lower() == "post" and kwargs.get("chunk"):
            self.headers["Content-Length"] = str(len(kwargs.get('data') or ""))
        r = await self.requests.request(kwargs['method'], kwargs['url'], headers=self.headers, cookies=self.cookies, data=kwargs.get('data'))
        if r.status_code == 403 and r.headers.get('X-CSRF-TOKEN'):
            self.headers['X-CSRF-TOKEN'] = r.headers.get('X-CSRF-TOKEN')
            return await self.request(**kwargs)
        elif not r.status_code == 200:
            if not kwargs.get('noerror'):
                raise BadStatus(f'Got status {r.status_code} from {kwargs["url"]} data: {r.text}')
        if self.debug:
            print(kwargs['method'], kwargs['url'], r.status_code, r.text)
        return r

    def login(self, cookie):
        """
        Saves the cookie for later sent requests.
        :param cookie: A roblox cookie
        :return: None
        """
        cookies = {
            '.ROBLOSECURITY': cookie
        }
        r = requests.get('https://www.roblox.com/game/GetCurrentUser.ashx', cookies=cookies, headers=self.headers)
        if r.text != 'null':
            self.cookies = cookies
        else:
            raise NotAuthenticated("Cookie was incorrect.")

