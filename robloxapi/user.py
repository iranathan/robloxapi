import json
from .utils.errors import *
from .utils.classes import *
from .detaileduser import *
from .gamepass import *
from .group import *
from bs4 import BeautifulSoup


class User:
    def __init__(self, request, roblox_id, roblox_name):
        self.request = request
        self.id = roblox_id
        self.name = roblox_name

    async def send_message(self, subject: str, body: str) -> Message:
        data = {
            'recipientid': self.id,
            'subject': subject,
            'body': body
        }
        r = await self.request.request(url='https://www.roblox.com/messages/send', method='POST', data=json.dumps(data))
        return Message(recipient_id, subject, message, r.json()['success'])

    async def get_role_in_group(self, group_id: int) -> Role:
        r = await self.request.request(url=f'https://groups.roblox.com/v1/users/{self.id}/groups/roles', method='GET')
        data = r.json()
        user_role = None
        for group in data['data']:
            if group['group']['id'] == group_id:
                user_role = group
                break
        if not user_role:
            raise NotFound('The user is not in that group.')
        return Role(user_role['role']['id'], user_role['role']['name'], user_role['role']['rank'], user_role['role']['memberCount'])

    async def get_friends(self):
        r = await self.request.request(url=f'https://friends.roblox.com/v1/users/{self.id}/friends', method="GET")
        data = r.json()
        friends = []
        for friend in data['data']:
            friends.append(User(self.request, friend['id'], friend['name']))
        return friends

    async def block(self) -> int:
        data = json.dumps({
            'blockeeId': self.id
        })
        r = await self.request.request(url=f'https://www.roblox.com/userblock/blockuser', data=data, method='POST')
        return r.status_code

    async def unblock(self) -> int:
        data = json.dumps({
            'blockeeId': self.id
        })
        r = await self.request.request(url='https://www.roblox.com/userblock/unblockuser', data=data, method='POST')
        return r.status_code

    async def follow(self) -> int:
        r = await self.request.request(url=f'https://friends.roblox.com/v1/users/{self.id}/follow', method='POST')
        return r.status_code

    async def unfollow(self) -> int:
        r = await self.request.request(url=f'https://friends.roblox.com/v1/users/{self.id}/unfollow', method='POST')
        return r.status_code

    # TODO: Status, Join date, Follower count, Friend count and Following count
    async def get_detailed_user(self) -> DetailedUser:
        r = await self.request.request(url=f'https://www.roblox.com/users/{self.id}/profile', method="GET")
        soup = BeautifulSoup(r.text, "html.parser")
        avatar = soup.find('span', {'class': 'avatar-card-link avatar-image-link'}).img['src']
        blurb = soup.find('div', {'class': 'profile-about-content'}).pre.span.text
        dates = soup.find('ul', {'class': 'profile-stats-container'})
        join_date = dates.li.find('p', {'class': 'text-lead'}).text
        return DetailedUser(self.request, self.id, self.name, blurb, join_date, avatar)

    async def get_gamepasses(self, cursor='') -> list:
        r = await self.request.request(url=f'https://www.roblox.com/users/inventory/list-json?assetTypeId=34&itemsPerPage=100&pageNumber=1&userId={self.id}&cursor={cursor}', method="GET")
        data = r.json()
        gamepasses = []
        for gamepass in data['Data']['Items']:
            if gamepass['Creator']['Type'] == 1:
                creator = User(self.request, gamepass['Creator']['Id'], gamepass['Creator']['Name'])
            elif gamepass['Creator']['Type'] == 2:
                # TODO: Figure out something
                creator = None
            price = gamepass['Product']['PriceInRobux'] if gamepass.get('Product') else None
            sale = gamepass['Product']['IsForSale'] if gamepass.get('Product') else None
            gamepasses.append(Gamepass(self.request, gamepass['Item']['AssetId'], gamepass['Item']['Name'], price, gamepass['Thumbnail']['Url'], creator, sale))
        return gamepasses

    async def has_gamepass(self, gamepass_id: int) -> bool:
        gamepasses = await self.get_gamepasses()
        owned = False
        for gamepass in gamepasses:
            if gamepass.id == gamepass_id:
                owned = True
                break
        return owned
