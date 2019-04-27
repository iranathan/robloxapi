import requests
from json import loads
from json import dumps
import requests
from .xcsrf import get_xcsrf
class request:

    def __init__(self, cookie=None):
        self.auth = False
        self.xcsrf = get_xcsrf()
        self._request = requests
        self.cookies = {}
        if cookie:
            self.login(cookie)
            


    def request(self, **kwargs):
        if not 'method' in kwargs: kwargs['method'] = 'GET'
        if not 'headers' in kwargs: kwargs['headers'] = self.get_headers()
        if not 'data' in kwargs: kwargs['data'] = None
        if 'X-CSRF-TOKEN' in kwargs: kwargs['headers']['X-CSRF-TOKEN'] = kwargs['X-CSRF-TOKEN']
        url = kwargs['url']
        method = kwargs['method']
        r = self._request.request(method, url, cookies=self.cookies, headers=kwargs['headers'], data=dumps(kwargs['data']))
        if r.status_code == 200:
            return r.text
        elif r.status_code == 403:
            if r.headers['X-CSRF-TOKEN']:
                self.xcsrf = r.headers['X-CSRF-TOKEN']
                kwargs['X-CSRF-TOKEN'] = self.xcsrf
                self.request(kwargs)
            else:
                raise Exception('Failed to get xcsrf token.')
        else:
            raise Exception('Error with request: ', r.text)
         


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
    
    def request_cookie():
        pass

        


    def login(self, cookie):
        url = 'https://www.roblox.com/game/GetCurrentUser.ashx'
        cookies = {
            '.ROBLOSECURITY': cookie
        }
        r = requests.get(url, headers=self.get_headers(), cookies=cookies)
        if r.text == 'null':
            raise Exception('Unable to log in.')
            self.cookies = {}
            self.auth = False
        else:
            self.cookies = cookies
            self.auth = True





        
        
   
