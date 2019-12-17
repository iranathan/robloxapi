import json
from .utils.errors import *
from .utils.classes import *


class User:
    def __init__(self, request, roblox_id, roblox_name):
        self.request = request
        self.id = roblox_id
        self.name = roblox_name

    async def send_message(self, subject, body) -> dict:
        data = {
            'recipientid': self.id,
            'subject': subject,
            'body': body
        }
        r = await self.request.request(url='https://www.roblox.com/messages/send', method='POST', data=json.dumps(data))
        return Message(recipient_id, subject, message, r.json()['success'])

    async def get_role_in_group(self, group_id):
        r = await self.request.request(url=f'https://groups.roblox.com/v1/users/{self.id}/groups/roles', method='GET')
        json = r.json()
        user_role = None
        for group in json['data']:
            if group['group']['id'] == group_id:
                user_role = group
                break
        if not user_role:
            raise NotFound('The user is not in that group.')
        return Role(user_role['role']['id'], user_role['role']['name'], user_role['role']['rank'], user_role['role']['memberCount'])
