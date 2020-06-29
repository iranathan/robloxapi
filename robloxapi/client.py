# Typings
from typing import List
# Packages
from .utils.request import *
from .utils.errors import *
from .group import *
from .user import *
from .traderequest import *
from .auth import *
import json as j
import asyncio


class Client:
    """
    Client
    """
    def __init__(self, cookie=None, debug=False):
        """
        Created a client.
        :param cookie: A roblox cookie to login with
        """
        self.request = Request(cookie, debug)

    async def get_self(self):
        """
        Gets the user the lib is logged into.
        :return: The user
        """
        if not ".ROBLOSECURITY" in self.request.cookies:
            raise NotAuthenticated("You must be authenticated to preform that action.")
        r = await self.request.request(url="https://www.roblox.com/my/profile", method="GET")
        data = r.json()
        return User(self.request, data["UserId"], data["Username"])

    async def get_trades(self) -> List[TradeRequest]:
        """
        Gets al trade requests.
        :return: List of trade requests
        """
        data = j.dumps({
            'startindex': 0,
            'statustype': 'inbound'
        })
        r = await self.request.request(url='https://www.roblox.com/my/money.aspx/getmyitemtrades', data=data, method='POST')
        data = json.loads(r.json()['d'])["Data"]
        trades = []
        for trade in data:
            t = json.loads(trade)
            trades.append(TradeRequest(self.request, t['Date'], t['Expires'], t['TradePartner'], t['TradePartnerID'], t['Status'], t['TradeSessionID']))
        return trades

    async def get_group(self, group_id: int) -> Group:
        """
        Gets a group.
        :param group_id: A roblox group id
        :return: The group class
        """
        r = await self.request.request(url=f'https://groups.roblox.com/v1/groups/{group_id}/', method='GET', noerror=True)
        if r.status_code != 200:
            return None
        json = r.json()
        return Group(self.request, json['id'], json['name'], json['description'], json['memberCount'], json['shout'], json['owner'].get('userId'), json['owner'].get('username'))

    async def get_user_by_username(self, roblox_name: str) -> User:
        """
        Gets a user using there username.
        :param roblox_name: The users username
        :return: The user
        """
        r = await self.request.request(url=f'https://api.roblox.com/users/get-by-username?username={roblox_name}', method="GET", noerror=True)
        json = r.json()
        if r.status_code != 200 or not json.get('Id') or not json.get('Username'):
            return None
        return User(self.request, json['Id'], json['Username'])

    async def get_user_by_id(self, roblox_id: int) -> User:
        """
        Gets a user using there id.
        :param roblox_id: The users id
        :return: The user
        """
        r = await self.request.request(url=f'https://api.roblox.com/users/{roblox_id}', method="GET", noerror=True)
        json = r.json()
        if r.status_code != 200 or not json.get('Id') or not json.get('Username'):
            return None
        return User(self.request, json['Id'], json['Username'])

    async def get_user(self, name=None, id=None) -> User:
        """
        Does the same thing as get_user_by_username and get_user_by_id just with optional arguments
        :param name: Not required the users username
        :param id: Not required the users id
        :return: The user
        """
        if name:
            return await self.get_user_by_username(name)
        if id:
            return await self.get_user_by_id(id)
        return None

    async def get_friends(self) -> List[User]:
        """
        Gets the logged in users friends
        :return: A list of users
        """
        me = await self.get_self()
        r = await self.request.request(url=f'https://friends.roblox.com/v1/users/{me.id}/friends', method="GET")
        data = r.json()
        friends = []
        for friend in data['data']:
            friends.append(User(self.request, friend['id'], friend['name']))
        return friends

    async def change_status(self, status: str) -> int:
        """
        Changes the logged in users status
        :param status:
        :return: StatusCode
        """
        data = {'status': str(status)}
        r = await self.request.request(url='https://www.roblox.com/home/updatestatus', method='POST', data=j.dumps(data))
        return r.status_code

    async def login(self, username=None, password=None, key=None):
        """
        Logs in to a roblox account with 2captcha
        :param username: The account username
        :param password: The account password
        :param key: 2captcha token
        :return: None
        """
        client = Auth(self.request)
        if not username or not password:
            raise AuthenticationError("You did not supply a username or password")
        status, cookies = await client.login(username, password)
        if status == 200 and ".ROBLOSECURITY" in cookies:
            self.request = Request(cookies[".ROBLOSECURITY"])
        if not key:
            raise CaptchaEncountered("2captcha required.")
        else:
            captcha = Captcha(self.request, key)
            data, status = await captcha.create_task()
            token = ''
            if status == 200:
                while True:
                    r, s = await captcha.check_task(data["request"])
                    if r['request'] != "CAPCHA_NOT_READY":
                        token = r['request']
                        break
                    await asyncio.sleep(1.5)
        status, cookies = await client.login(username, password, token)
        if status == 200 and ".ROBLOSECURITY" in cookies:
            self.request = Request(cookies[".ROBLOSECURITY"])
