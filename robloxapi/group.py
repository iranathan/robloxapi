import json
import logging
from bs4 import BeautifulSoup
from .utils.errors import *


class Group:
    def __init__(self, request):
        self.request = request

    async def get_funds(self, group_id: int) -> int:
        r = await self.request.request(url=f'https://economy.roblox.com/v1/groups/{group_id}/currency', method='GET')
        return int(r.json().get('robux'))

    async def search_group(self, keyword: str, show=100) -> list:
        r = await self.request.request(url=f'https://www.roblox.com/search/groups/list-json?keyword={keyword}&maxRows={show}&startRow=0', method='GET')
        return r.json().get('GroupSearchResults')

    async def get_group(self, group_id: int) -> dict:
        r = await self.request.request(url=f'https://groups.roblox.com/v1/groups/{group_id}', method='GET')
        return r.json()

    async def get_group_roles(self, group_id: int) -> list:
        r = await self.request.request(url=f'https://groups.roblox.com/v1/groups/{group_id}/roles', method='GET')
        return r.json().get('roles')

    async def get_role_in_group(self, group_id: int, rbx_id: int) -> str:
        r = await self.request.request(url=f'https://www.roblox.com/Game/LuaWebService/HandleSocialRequest.ashx?method=GetGroupRank&playerid={rbx_id}&groupId={group_id}', method='GET')
        return r.text

    async def send_payout(self, group_id: int, user_id: int, amount: int) -> dict:
        payout_data = {
            'PayoutType': 'FixedAmount',
            'Recipients': [
                {
                    'recipientId': user_id,
                    'recipientType': 'User',
                    'amount': amount,
                }
            ]
        }
        r = await self.request.request(url=f'https://groups.roblox.com/v1/groups/{group_id}/payouts', data=json.dumps(payout_data), method='POST')
        return r.json()

    async def get_join_requests(self, groupid: int) -> list:
        r = await self.request.request(url=f'https://www.roblox.com/groups/{groupid}/joinrequests-html?pageNum=1', method='GET')
        soup = BeautifulSoup(r.text, 'html.parser')
        found = soup.find('tbody')
        tr = found.find_all('tr')
        del tr[-1]
        requests = []
        for request in tr:
            requests.append({
                'JoinId': request.find('span', {"class": "btn-control btn-control-medium accept-join-request"})[
                    'data-rbx-join-request'],
                'User': {
                    'AvatarPicture': request.td.span.img['src'],
                    'Username': request.find('a').text,
                    'Id': re.findall(r'\b\d+\b', request.find('a')['href']),
                    'ProfileLink': request.find('a')['href']
                }
            })
        return requests

    # thanks to Auxority i ~stole~ got the api from him
    async def get_audit_log(self, group_id: int):
        r = await self.request.request(url=f'https://groups.roblox.com/v1/groups/{group_id}/audit-log?sortOrder=Asc&limit=100')
        return r.json()

    async def handle_join_request(self, request_id: int or str, accept: bool) -> dict:
        data = {
            'groupJoinRequestId': request_id
        }
        if accept:
            data['accept'] = True
        r = await self.request.request(url='https://www.roblox.com/group/handle-join-request', method='POST', data=json.dumps(data))
        return r.json()

    async def accept_join_request(self, request_id: int or str) -> dict:
        return await self.handle_join_request(request_id, True)

    async def decline_join_request(self, request_id: int or str) -> dict:
        return await self.handle_join_request(request_id, False)

    async def post_shout(self, group_id: int, message: str) -> dict:
        data = {'message': message}
        r = await self.request.request(url=f'https://groups.roblox.com/v1/groups/{group_id}/status', method='PATCH', data=json.dumps(data))
        return r.json()

    async def get_group_roles(self, group_id: int) -> list:
        r = await self.request.request(url=f'https://groups.roblox.com/v1/groups/{group_id}/roles', method='GET')
        return r.json().get('roles')

    async def get_wall(self, group_id: int, limit=10) -> list:
        r = await self.request.request(url=f'https://groups.roblox.com/v2/groups/{group_id}/wall/posts?limit={limit}', method='GET')
        return r.json().get('data')

    async def set_rank(self, group_id: int, target_id: int, role_id: int) -> dict:
        r = await self.request.request(url=f'https://www.roblox.com/groups/api/change-member-rank?groupId={group_id}&newRoleSetId={role_id}&targetUserId={target_id}', method='POST')
        return r.json()

    async def set_rank_by_id(self, group_id: int, target_id: int, role_id) -> dict:
        roles = await self.get_group_roles(group_id)
        picked_role = None
        for role in roles:
            if role['rank'] == role_id:
                picked_role = role['id']
        if not picked_role:
            raise NotFound('The role was not found. (set_rank_by_id)')
        return await self.set_rank(group_id, target_id, picked_role)

    async def exile(self, group_id: int, roblox_id: int) -> dict:
        r = await self.request.request(url=f'https://groups.roblox.com/v1/groups/{group_id}/users/{roblox_id}', method='DELETE')
        return r.json()
