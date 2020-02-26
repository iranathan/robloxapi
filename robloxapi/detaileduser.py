import json
from .utils.errors import *
from .utils.classes import Message, Role
from .gamepass import *
from .group import *
from .user import *
from bs4 import BeautifulSoup


class DetailedUser:
    """
    Represents a user with more detail.
    """
    def __init__(self, request, roblox_id, roblox_name, blurb, join_date, avatar_url):
        """
        Construct a new user class with more detail.
        :param request: Used to send requests
        :param roblox_id: The id of the roblox user
        :param roblox_name: The name of the roblox user
        :param blurb: The blurb of the roblox user
        :param join_date: The date when the roblox user joined
        :param avatar_url: A url of a photo of the roblox user
        """
        self.request = request
        self.id = roblox_id
        self.name = roblox_name
        self.blurb = blurb
        self.join_date = join_date
        self.avatar_url = avatar_url

    async def send_message(self, subject: str, body: str) -> Message:
        """
        Sends a message to the user on roblox.
        :param subject: The subject of the message
        :param body: The body of the message
        :return: Message class
        """
        data = {
            'recipientid': self.id,
            'subject': subject,
            'body': body
        }
        r = await self.request.request(url='https://www.roblox.com/messages/send', method='POST', data=json.dumps(data))
        return Message(recipient_id, subject, message, r.json()['success'])

    async def get_role_in_group(self, group_id: int) -> Role:
        """
        Gets the users role in a group.
        :param group_id: The group to get the role from
        :return: Role class: The role the user has
        """
        r = await self.request.request(url=f'https://groups.roblox.com/v1/users/{self.id}/groups/roles', method='GET')
        data = r.json()
        user_role = None
        for group in data['data']:
            if group['group']['id'] == group_id:
                user_role = group
                break
        if not user_role:
            raise NotFound('The user is not in that group.')
        return Role(user_role['role']['id'], user_role['role']['name'], user_role['role']['rank'],
                    user_role['role']['memberCount'])

    async def get_friends(self):
        """
        Gets all of the users friends.
        :return: List of user classes
        """
        r = await self.request.request(url=f'https://friends.roblox.com/v1/users/{self.id}/friends', method="GET")
        data = r.json()
        friends = []
        for friend in data['data']:
            friends.append(User(self.request, friend['id'], friend['name']))
        return friends

    async def block(self) -> int:
        """
        Blocks the user.
        :return: StatusCode
        """
        data = json.dumps({
            'blockeeId': self.id
        })
        r = await self.request.request(url=f'https://www.roblox.com/userblock/blockuser', data=data, method='POST')
        return r.status_code

    async def unblock(self) -> int:
        """
        Unblocks the user.
        :return: StatusCode
        """
        data = json.dumps({
            'blockeeId': self.id
        })
        r = await self.request.request(url='https://www.roblox.com/userblock/unblockuser', data=data, method='POST')
        return r.status_code

    async def follow(self) -> int:
        """
        Follows the user
        :return: StatusCode
        """
        r = await self.request.request(url=f'https://friends.roblox.com/v1/users/{self.id}/follow', method='POST')
        return r.status_code

    async def unfollow(self) -> int:
        """
        Unfollows the user.
        :return: StatusCode
        """
        r = await self.request.request(url=f'https://friends.roblox.com/v1/users/{self.id}/unfollow', method='POST')
        return r.status_code

    async def get_gamepasses(self, cursor='') -> List[Gamepass]:
        """
        Gets the users gamepasses.
        :param cursor: Not required used by the lib to get the next page
        :return: List of gamepasses
        """
        r = await self.request.request(
            url=f'https://www.roblox.com/users/inventory/list-json?assetTypeId=34&itemsPerPage=100&pageNumber=1&userId={self.id}&cursor={cursor}',
            method="GET")
        data = r.json()
        gamepasses = []
        creator = None
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
        """
        Checks if the user has a gamepass
        :param gamepass_id: The id of the gamepass to check for
        :return: True/False
        """
        gamepasses = await self.get_gamepasses()
        owned = False
        for gamepass in gamepasses:
            if gamepass.id == gamepass_id:
                owned = True
                break
        return owned
