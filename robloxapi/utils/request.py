import json
import requests
from .xcsrf import get_xcsrf
import logging
import aiohttp


class request:

    def __init__(self, cookie=None):
        self.auth = False
        self.session = aiohttp.ClientSession()
        self.cookies = {}
        self.xcsrf = get_xcsrf()
        if cookie:
            self.login(cookie)

    async def request(self, **kwargs):
        if not 'method' in kwargs: kwargs['method'] = 'GET'
        if not 'headers' in kwargs: kwargs['headers'] = self.get_headers()
        if not 'data' in kwargs: kwargs['data'] = None
        if 'X-CSRF-TOKEN' in kwargs: kwargs['headers']['X-CSRF-TOKEN'] = kwargs['X-CSRF-TOKEN']
        if not 'allow_redirects' in kwargs: kwargs['allow_redirects'] = False
        url = kwargs['url']
        method = kwargs['method']
        if kwargs['data'] == None:
            kwargs['data'] = b''
        else:
            kwargs['data'] = str.encode(kwargs['data'])
        async with self.session.request(method, url, data=str.encode(kwargs['data']), headers=kwargs['headers']) as response:
            if response.status == 200:
                return await response.text()
            elif response.status == 403:
                if response.headers['X-CSRF-TOKEN']:
                    self.xcsrf = response.headers['X-CSRF-TOKEN']
                    kwargs['X-CSRF-TOKEN'] = self.xcsrf
                    return await self.request(**kwargs)
                else:
                    logging.error('Failed to request to: ' + url + ' Failed to get xcsrf (403)')
                    return {}
            else:
                logging.error(f'Failed with request. Check your cookie ({response.status})')
                return {}

    def get_headers(self):
        return {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:66.0) Gecko/20100101 Firefox/66.0',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.5',
        'Content-Type': 'application/json;charset=utf-8',
        'Origin': 'https://www.roblox.com',
        'X-CSRF-TOKEN': self.xcsrf,
        'DNT': '1',
        }

    async def login(self, cookie):
        url = 'https://www.roblox.com/game/GetCurrentUser.ashx'
        cookies = {
            '.ROBLOSECURITY': cookie
        }
        async with self.session.get(url, headers=get_headers()) as response:
            data = await response.text()
            if data == 'null':
                logging.warning('Failed to login. Using robloxapi without auth.')
            else:
                self.session = aiohttp.ClientSession(cookies=cookies, raise_for_status=False)


