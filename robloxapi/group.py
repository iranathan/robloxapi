import json
import logging
import re
import asyncio
from typing import List, Tuple
from bs4 import BeautifulSoup
from .utils.errors import RoleError, NotFound
from .utils.classes import Role, Shout, WallPost, Action
from .joinrequest import JoinRequest
from .groupmember import GroupMember
from .user import User
from .auth import Auth


class Group:
    """
    Represents a group.
    """
    def __init__(self, request, group_id, group_name, description, member_count, shout, owner_id=None, owner_username=None):
        """
        Construct a new group class.
        :param request: Used to send requests
        :param group_id: The id of the group
        :param group_name: The name of the group
        :param description: The group description
        :param member_count: The amount of members in a group
        :param shout: The group shout
        :param owner_id: The id of the owner
        :param owner_username: The username of the owner
        """
        self.request = request
        self.id = group_id
        self.name = group_name
        self.description = description
        if owner_id and owner_username:
            self.owner = User(self.request, owner_id, owner_username)
        self.member_count = member_count
        self.shout = shout

    async def pay(self, user_id: int, amount: int) -> int:
        """
        Pays a user.
        :param user_id: The user to pay
        :param amount: How much to pay the user
        :return: StatusCode
        """
        data = json.dumps({
            "PayoutType": "FixedAmount",
            "Recipients": [
                {
                    "recipientId": user_id,
                    "recipientType": "User",
                    "amount": amount
                }
            ]
        })
        r = await self.request.request(url=f'https://groups.roblox.com/v1/groups/{self.id}/payouts', data=data, method="POST")
        return r.status_code

    async def exile(self, user_id: int) -> int:
        """
        Exiles a user from the group.
        :param user_id: The users id
        :return: StatusCode
        """
        r = await self.request.request(url=f'https://groups.roblox.com/v1/groups/{self.id}/users/{user_id}', method='DELETE')
        return r.status_code

    async def set_rank(self, user_id: int, rank_id: int) -> int:
        """
        Set a users rank in the group.
        :param user_id: The users id
        :param rank_id: The rank id
        :return: StatusCode
        """
        data = json.dumps({
            'roleId': rank_id
        })
        r = await self.request.request(url=f'https://groups.roblox.com/v1/groups/{self.id}/users/{user_id}', method="PATCH", data=data)
        return r.status_code

    async def promote(self, user_id: int) -> Tuple[Role, Role]:
        """
        Moves the users role up by one.
        :param user_id: The users id
        :return: oldrole & newrole in a tuple
        """
        return await self.change_rank(user_id, 1)

    async def demote(self, user_id: int) -> Tuple[Role, Role]:
        """
        Moves the users role down by one.
        :param user_id: The users id
        :return: oldrole & newrole in a tuple
        """
        return await self.change_rank(user_id, -1)

    async def change_rank(self, user_id: int, change: int) -> Tuple[Role, Role]:
        """
        Changes the rank down or up by a specified amount.
        :param user_id: The users id
        :param change: How much to change the users role by (-5) (5)
        :return: oldrole & newrole in a tuple
        """
        roles = await self.get_group_roles()
        roles.sort(key=lambda r: r.rank)
        role = await self.get_role_in_group(user_id)
        user_role = -1
        for r in roles:
            user_role = user_role + 1
            if r.id == role.id:
                break
        new_user_role = user_role + change
        if len(roles) < new_user_role or int(roles[new_user_role].rank) == 255:
            raise RoleError("The role is over 255 or does not exist")
        await self.set_rank(user_id, roles[new_user_role].id)
        return role, roles[new_user_role]

    async def set_rank_by_id(self, user_id: int, role_id: int) -> int:
        """
        Sets the users role using a role id.
        :param user_id: The users id
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
        return await self.set_rank(user_id, choose.id)

    async def get_group_roles(self) -> List[Role]:
        """
        Get all of the group roles.
        :return: A list of Role classes
        """
        r = await self.request.request(url=f'https://groups.roblox.com/v1/groups/{self.id}/roles', method='GET')
        roles = []
        for role in r.json().get('roles'):
            roles.append(Role(role['id'], role['name'], role['rank'], role['memberCount']))
        roles.sort(key=lambda r: r.rank)
        return roles

    async def get_role_in_group(self, user_id) -> Role:
        """
        Get a users role in a group.
        :param user_id: The users id
        :return: A role class
        """
        r = await self.request.request(url=f'https://groups.roblox.com/v1/users/{user_id}/groups/roles', method='GET')
        data = r.json()
        user_role = None
        for group in data['data']:
            if group['group']['id'] == self.id:
                user_role = group
                break
        if not user_role:
            raise NotFound('The user is not in that group.')
        return Role(user_role['role']['id'], user_role['role']['name'], user_role['role']['rank'], user_role['role']['memberCount'])

    async def post_shout(self, message: str) -> Shout:
        """
        Post a shout to a group.
        :param message: The message to post
        :return: A shout class
        """
        data = {'message': message}
        r = await self.request.request(url=f'https://groups.roblox.com/v1/groups/{self.id}/status', method='PATCH', data=json.dumps(data))
        shout = r.json()
        return Shout(message, shout['poster']['username'], shout['poster']['userId'], shout['created'], shout['updated'])

    async def get_funds(self) -> int:
        """
        Get the amount of robux a group has.
        :return: The amount of robux as an int
        """
        r = await self.request.request(url=f'https://economy.roblox.com/v1/groups/{self.id}/currency', method='GET')
        return int(r.json().get('robux'))

    # TODO: Use https://groups.roblox.com/v1/groups/{groupId}/join-requests
    async def get_join_requests(self) -> List[JoinRequest]:
        """
        Gets the join requests of a group.
        :return: A list of Join request classes.
        """
        r = await self.request.request(url=f"https://groups.roblox.com/v1/groups/{self.id}/join-requests/", method="GET")
        data = r.json()
        requests = []
        for request in data["data"]:
            requests.append(JoinRequest(self.request, self.id, request["requester"]["username"], request["requester"]["userId"]))
        return requests

    async def get_audit_logs(self, action=None):
        """
        Gets actions in the audit log.
        :param action: Filter witch action.
        :return:
        """
        r = await self.request.request(url=f"https://groups.roblox.com/v1/groups/{self.id}/audit-log?actionType={action or 'all'}&limit=100&sortOrder=Asc", method="GET")
        data = r.json()
        logs = []
        for a in data['data']:
            actor = User(self.request, a["actor"]["user"]["userId"], a["actor"]["user"]["username"])
            description = None
            target = None
            if a['actionType'] == "Delete Post":
                description = WallPost(a["description"]["PostDesc"], User(self.request, a["description"]["TargetId"], a["description"]["TargetName"]))
            if a['actionType'] == "Remove Member":
                description = User(self.request, a["description"]["TargetId"], a["description"]["TargetName"])
            if a['actionType'] == "Accept Join Request" or a['actionType'] == "Decline Join Request":
                description = JoinRequest(self.request, self.id, a["description"]["TargetName"], a["description"]["TargetId"])
            if a['actionType'] == "Post Status":
                description = Shout(a["description"]["Text"], actor.name, actor.id, a["created"], a["created"])
            if a['actionType'] == "Change Rank":
                description = (Role(a["description"]["OldRoleSetId"], a["description"]["OldRoleSetName"]), Role(a["description"]["NewRoleSetId"], a["description"]["NewRoleSetName"]))
                target = User(self.request, a["description"]["TargetId"], a["description"]["TargetName"])
            logs.append(Action(a['actionType'], actor, description, target))
        return logs

    async def get_members(self):
        """
        Get all members of a group.
        :return: A list of user classes
        """
        cursor = ""
        while True:
            r = await self.request.request(url=f"https://groups.roblox.com/v1/groups/{self.id}/users?limit=100&sortOrder=Desc&cursor={cursor}", method="GET")
            response = r.json()
            for user in response['data']:
                yield GroupMember(self.request, user["user"]["userId"], user["user"]["username"], self.id, Role(user['role']['id'], user['role']['name'], user['role']['rank'], user['role']['memberCount']))
            if not response["nextPageCursor"]:
                break
            cursor = response["nextPageCursor"]
        return

    async def join(self, captcha: str) -> int:
        """
        Join a group.
        :param captcha: A 2captcha token to solve the captcha.
        :return: StatusCode
        """
        auth = Captcha(self.request, captcha, pkey="63E4117F-E727-42B4-6DAA-C8448E9B137F")
        token = ''
        data, status = await auth.create_task()
        if status == 200:
            while True:
                r, s = await auth.check_task(data["request"])
                if r['request'] != "CAPCHA_NOT_READY":
                    token = r['request']
                    break
                await asyncio.sleep(1.5)
        data = json.dumps({
            'captchaProvider': 'PROVIDER_ARKOSE_LABS',
            'captchaToken': token
        })
        r = await self.request.request(url=f'https://groups.roblox.com/v1/groups/{self.id}/users', data=data, method="POST")
        return r.status_code

    async def leave(self) -> int:
        """
        Leaves a group
        :return: StatusCode
        """
        r = await self.request.request(url="https://groups.roblox.com/v1/groups/3788537/users/109503558", method="DELETE")
        return r.status_code
