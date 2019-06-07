import requests
from json import loads
from json import dumps
import json
import requests
from .xcsrf import get_xcsrf
from .Errors import AuthError
import logging


class request:

    def __init__(self, cookie=None, debug=False, ready_event=None):
        self.auth = False
        self.xcsrf = get_xcsrf()
        self._request = requests
        self.cookies = {}
        self.debug = debug
        self.ready_event = ready_event
        self.login(cookie)
            
    

    def request(self, **kwargs):
        if not 'response' in kwargs: kwargs['response'] = False
        if not 'method' in kwargs: kwargs['method'] = 'GET'
        if not 'headers' in kwargs: kwargs['headers'] = self.get_headers()
        if not 'data' in kwargs: kwargs['data'] = None
        if kwargs['method'] == 'POST' and str(self.cookies) == '{}': raise AuthError('You must login to use that function')
        if 'X-CSRF-TOKEN' in kwargs: kwargs['headers']['X-CSRF-TOKEN'] = kwargs['X-CSRF-TOKEN']
        url = kwargs['url']
        method = kwargs['method']
        r = self._request.request(method, url, cookies=self.cookies, headers=kwargs['headers'], data=kwargs['data'])
        if kwargs['response']:
            return r
        if self.debug is True:
            logging.debug(f'{url} {method} {r.status_code}')
        if r.status_code == 200:
            return r.text
        elif r.status_code == 403:
            if 'X-CSRF-TOKEN' in r.headers:
                self.xcsrf = r.headers['X-CSRF-TOKEN']
                kwargs['X-CSRF-TOKEN'] = self.xcsrf
                res = self.request(**kwargs)
                return res
            else:
                logging.error('Failed to get xcsrf token.')
                return {}
        else:
            logging.error('Error with request code: ' + str(r.status_code) + ' data:' + r.text)
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
    
    def request_cookie():
        pass

        


    def login(self, cookie):
        url = 'https://www.roblox.com/game/GetCurrentUser.ashx'
        cookies = {
            '.ROBLOSECURITY': cookie
        }
        r = requests.get(url, headers=self.get_headers(), cookies=cookies)
        if r.text == 'null':
            logging.warning('Failed to login using robloxapi without auth.')
            self.cookies = {}
            self.auth = False
            self.user_info = {}
            if self.ready_event:
                self.ready_event(user=None)
        else:
            self.cookies = cookies
            self.auth = True
            info = self.request(url='https://www.roblox.com/my/profile', method='GET')
            info = json.loads(info)
            self.user_info = {
                'username': info['Username'],
                'Id': info['UserId'],
                'Robux': info['Robux']
            }
            if self.ready_event:
                self.ready_event(user=self.user_info)
