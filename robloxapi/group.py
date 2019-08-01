import json
from bs4 import BeautifulSoup


class Group:
    def __init__(self, request):
        self.request = request

    async def get_funds(self, groupid) -> int:
        r = await self.request.request(url=f'https://economy.roblox.com/v1/groups/{groupid}/currency', method='GET')
        return int(r.json().get('robux'))

    async def search_group(self, keyword, show=100) -> list:
        r = await self.request.request(url=f'https://www.roblox.com/search/groups/list-json?keyword={keyword}&maxRows={show}&startRow=0', method='GET')
        return r.json().get('GroupSearchResults')

    async def get_group(self, groupid) -> dict:
        r = await self.request.request(url=f'https://groups.roblox.com/v1/groups/{groupid}', method='GET')
        return r.json()

    async def get_group_roles(self, groupid) -> list:
        r = await self.request.request(url=f'https://groups.roblox.com/v1/groups/{groupid}/roles', method='GET')
        return r.json().get('roles')

    async def get_role_in_group(self, groupid, id) -> str:
        r = await self.request.request(url=f'https://www.roblox.com/Game/LuaWebService/HandleSocialRequest.ashx?method=GetGroupRank&playerid={id}&groupId={groupid}', method='GET')
        return r.text

    async def send_payout(self, groupid, userid, amount) -> dict:
        payout_data = {
            'PayoutType': 'FixedAmount',
            'Recipients': [
                {
                    'recipientId': userid,
                    'recipientType': 'User',
                    'amount': amount,
                }
            ]
        }
        r = await self.request.request(url=f'https://groups.roblox.com/v1/groups/{groupid}/payouts', data=json.dumps(payout_data), method='POST')
        return r.json()

    async def get_join_requests(self, groupid) -> list:
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

    async def handle_join_request(self, requestid, accept) -> dict:
        data = {
            'groupJoinRequestId': requestid
        }
        if accept:
            data['accept'] = True
        r = await self.request.request(url='https://www.roblox.com/group/handle-join-request', method='POST', data=json.dumps(data))
        return r.text

    async def accept_join_request(self, requestid) -> dict:
        return await self.handle_join_request(requestid, True)

    async def decline_join_request(self, requestid) -> dict:
        return await self.handle_join_request(requestid, False)

    async def post_shout(self, groupid, message) -> dict:
        data = {'message': str(message)}
        r = await self.request.request(url=f'https://groups.roblox.com/v1/groups/{groupid}/status', method='PATCH')
        return r.json()

    # TODO: get_audit_log

    async def get_wall(self, groupid, limit=10) -> list:
        r = await self.request.request(url=f'https://groups.roblox.com/v2/groups/{groupid}/wall/posts?limit={limit}', method='GET')
        return r.json().get('data')

    async def setrank(self, groupid, targetid, roleid) -> dict:
        r = await self.request.request(url=f'https://www.roblox.com/groups/api/change-member-rank?groupId={groupid}&newRoleSetId={roleid}&targetUserId={targetid}', method='POST')
        return r.json()

    async def exile(self, groupid, id) -> dict:
        r = await self.request.request(url=f'https://groups.roblox.com/v1/groups/{groupid}/users/{id}', method='DELETE')
        return r.json()
