import http3, logging


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
        self.auth = False
        self.user = {}
        if cookie:
            loop = asyncio.get_event_loop()
            loop.run_until_complete(self.login(cookie))
            loop.close()

    async def xcsrf(self):
        r = await self.requests.post('https://www.roblox.com/favorite/toggle')
        if r.headers['X-CSRF-TOKEN']:
            return r.headers['X-CSRF-TOKEN']
        else:
            return None

    async def request(self, **kwargs):
        if not 'method' in kwargs: kwargs['method'] = 'GET'
        r = await self.requests.request(kwargs['method'], kwargs['url'], headers=self.headers, cookies=self.cookies)
        if r.status_code == 403 and r.headers.get('X-CSRF-TOKEN'):
            self.headers['X-CSRF-TOKEN'] = r.headers.get('X-CSRF-TOKEN')
            return await request(**kwargs)
        elif r.status_code != 200:
            logging.error(f'Error with endpoint {kwargs["url"]} statuscode: {r.status_code}')
            return r
        return r

    async def login(self, cookie):
        cookies = {
            '.ROBLOSECURITY': cookie
        }
<<<<<<< HEAD
        r = await self.requests.get('https://www.roblox.com/game/GetCurrentUser.ashx', cookies=cookies, headers=self.headers)
        if r.text != 'null':
            self.auth = True
            self.user['Id'] = r.text
            self.cookies = cookies
        else:
            logging.warning('The cookie was incorrect. Using lib without auth.')
=======
        async with self.session.get(url, headers=self.get_headers()) as response:
            data = await response.text()
            if data == 'null':
                logging.warning('Failed to login. Using robloxapi without auth.')
            else:
                self.session = aiohttp.ClientSession(cookies=cookies, raise_for_status=False)


>>>>>>> bc3a5178ce571d20ba87949ccde1e397ece30090
