import json
import logging
from bs4 import BeautifulSoup
from .utils.errors import *
from .utils.classes import *
from .joinrequest import JoinRequest


class Group:
    def __init__(self, request, group_id, group_name, description, member_count, owner_id=None, owner_username=None):
        self.request = request
        self.id = group_id
        self.name = group_name
        self.description = description
        self.owner = {
            'id': owner_id,
            'name': owner_username
        }
        self.member_count = member_count

    async def exile(self, user_id: int) -> int:
        r = await self.request.request(url=f'https://groups.roblox.com/v1/groups/{self.id}/users/{user_id}', method='GET')
        return r.status_code

    async def set_rank(self, user_id: int, rank_id: int) -> int:
        r = await self.request.request(url=f'https://www.roblox.com/groups/api/change-member-rank?groupId={self.id}&newRoleSetId={rank_id}&targetUserId={user_id}', method='POST')
        return r.status_code

    # TODO: Promote & Demote

    async def set_rank_by_id(self, user_id: int, role_id: int) -> int:
        roles = await self.get_group_roles()
        choose = None
        for role in roles:
            if role.rank == role_id:
                choose = role
        if not choose:
            raise NotFound(f'Role {role_id} does not exist.')
        return await self.set_rank(user_id, choose.id)

    async def get_wall(self, limit=10):
        r = await self.request.request(url=f'https://groups.roblox.com/v2/groups/{self.id}/wall/posts?limit={limit}', method='GET')

    async def get_group_roles(self) -> list:
        r = await self.request.request(url=f'https://groups.roblox.com/v1/groups/{self.id}/roles', method='GET')
        roles = []
        for role in r.json().get('roles'):
            roles.append(Role(role['id'], role['name'], role['rank'], role['memberCount']))
        return roles

    async def post_shout(self, message: str) -> Shout:
        data = {'message': message}
        r = await self.request.request(url=f'https://groups.roblox.com/v1/groups/{group_id}/status', method='PATCH', data=json.dumps(data))
        json = r.json()
        return Shout(message, json['poster']['username'], json['poster']['userId'], json['created'], json['updated'])

    async def get_funds(self):
        r = await self.request.request(url=f'https://economy.roblox.com/v1/groups/{self.id}/currency', method='GET')
        return r.json().get('robux')

    # TODO: Use https://groups.roblox.com/v1/groups/{groupId}/join-requests
    async def get_join_requests(self):
        r = await self.request.request(url=f'https://www.roblox.com/groups/{self.id}/joinrequests-html', method='GET')
        soup = BeautifulSoup(r.text)
        container = soup.find('tbody').find_all('tr')
        del container[-1]
        requests = []
        for request in container:
            request_id = request.find('span', {"class": "btn-control btn-control-medium accept-join-request"})['data-rbx-join-request']
            roblox_avatar = request.td.span.img['src']
            roblox_name = request.find('a').text
            roblox_id = re.findall(r'\b\d+\b', request.find('a')['href'])
            requests.append(JoinRequest(self.request, request_id, roblox_name, roblox_id, roblox_avatar))
        return requests