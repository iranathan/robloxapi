import json
from bs4 import BeautifulSoup
from .utils.errors import *
from .utils.classes import Role
from typing import List, Tuple


class GroupMember:
    """
    Represents a member in a group.
    """
    def __init__(self, request, roblox_id, roblox_username, role, group_id):
        """
        Construct a new group member class.
        :param request: Used to send requests
        :param roblox_id: The group members roblox id
        :param roblox_username: The group members roblox username
        :param role: The group members role
        :param group_id: The group id
        """
        self.request = request
        self.id = roblox_id
        self.name = roblox_username
        self.role = role
        self.group_id = group_id

    async def exile(self) -> int:
        """
        Exile the user from the group
        :return: StatusCode
        """
        r = await self.request.request(url=f'https://groups.roblox.com/v1/groups/{self.group_id}/users/{self.id}', method="POST")
        return r.status_code

    async def set_rank(self, rank_id: int) -> int:
        """
        Set a users rank in the group.
        :param rank_id: The rank id
        :return: StatusCode
        """
        data = json.dumps({
            'roleId': rank_id
        })
        r = await self.request.request(url=f'https://groups.roblox.com/v1/groups/{self.group_id}/users/{self.id}', method="PATCH", data=data)
        return r.status_code

    async def set_rank_by_id(self, role_id: int) -> int:
        """
        Sets the users role using a role id.
        :param role_id: The role id (254, 1, etc)
        :return:
        """
        roles = await self.get_group_roles()
        choose = None
        for role in roles:
            if role.rank == role_id:
                choose = role
        if not choose:
            raise NotFound(f'Role {role_id} does not exist.')
        return await self.set_rank(choose.id)

    async def change_rank(self, change: int) -> Tuple[Role, Role]:
        """
        Changes the rank down or up by a specified amount.
        :param change: How much to change the users role by (-5) (5)
        :return: oldrole & newrole in a tuple
        """
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
        await self.set_rank(roles[new_user_role].id)
        return self.role, roles[new_user_role]

    async def promote(self) -> Tuple[Role, Role]:
        """
        Moves the users role up by one.
        :return: oldrole & newrole in a tuple
        """
        return await self.change_rank(1)

    async def demote(self) -> Tuple[Role, Role]:
        """
        Moves the users role down by one.
        :return: oldrole & newrole in a tuple
        """
        return await self.change_rank(-1)
