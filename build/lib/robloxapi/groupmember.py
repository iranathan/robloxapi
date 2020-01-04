import json
from bs4 import BeautifulSoup
from .utils.errors import *
from .utils.classes import *


class GroupMember:
    def __init__(self, request, roblox_id, roblox_username, group_id, role):
        self.request = request
        self.id = roblox_id
        self.name = roblox_username
        self.role = role
        self.group_id = group_id

    async def exile(self) -> int:
        r = await self.request.request(url=f'https://groups.roblox.com/v1/groups/{self.group_id}/users/{self.id}', method="POST")
        return r.status_code

    async def get_group_roles(self) -> list:
        r = await self.request.request(url=f'https://groups.roblox.com/v1/groups/{self.group_id}/roles', method='GET')
        roles = []
        for role in r.json().get('roles'):
            roles.append(Role(role['id'], role['name'], role['rank'], role['memberCount']))
        return roles

    async def set_rank(self, rank_id: int) -> int:
        data = json.dumps({
            'roleId': rank_id
        })
        r = await self.request.request(url=f'https://groups.roblox.com/v1/groups/{self.group_id}/users/{self.id}', method="PATCH", data=data)
        return r.status_code

    async def change_rank(self, change: int) -> int:
        roles = await self.get_group_roles()
        user_role = -1
        for r in roles:
            user_role = user_role + 1
            if r.id == self.role.id:
                break
        new_user_role = user_role + change
        print(roles[new_user_role].rank)
        if len(roles) < new_user_role or int(roles[new_user_role].rank) == 255:
            raise RoleError("The role is over 255 or does not exist")
        self.role = roles[new_user_role]
        return await self.set_rank(roles[new_user_role].id)

    async def promote(self) -> int:
        return await self.change_rank(1)

    async def demote(self) -> int:
        return await self.change_rank(-1)
