from .utils.request import *
from .utils.errors import *
from .group import *
from .user import *
from .traderequest import *
import json


class Client:
    def __init__(self, cookie=None):
        self.request = Request(cookie)

    async def get_trades(self) -> TradeRequest:
        data = json.dumps({
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
        r = await self.request.request(url=f'https://groups.roblox.com/v1/groups/{group_id}/', method='GET')
        if r.status_code != 200:
            raise NotFound('That group was not found.')
        json = r.json()
        return Group(self.request, json['id'], json['name'], json['description'], json['memberCount'], json['shout'], json['owner'].get('userId'), json['owner'].get('username'))

    async def get_user_by_username(self, roblox_name: str) -> User:
        r = await self.request.request(url=f'https://api.roblox.com/users/get-by-username?username={roblox_name}', method="GET")
        json = r.json()
        if not json.get('Id') or not json.get('Username'):
            raise NotFound('That user was not found.')
        return User(self.request, json['Id'], json['Username'])

    async def get_user_by_id(self, roblox_id: int) -> User:
        r = await self.request.request(url=f'https://api.roblox.com/users/{roblox_id}', method="GET")
        json = r.json()
        if r.status_code != 200:
            raise NotFound('That user was not found.')
        return User(self.request, json['Id'], json['Username'])

    async def get_user(self, name=None, id=None):
        if name:
            return await self.get_user_by_username(name)
        if id:
            return await self.get_user_by_id(id)
        if not id and not name:
            return None

    async def change_status(self, status: str) -> int:
        data = {'status': str(status)}
        r = await self.request.request(url='https://www.roblox.com/home/updatestatus', method='POST', data=json.dumps(data))
        return r.status_code