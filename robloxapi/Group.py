from bs4 import BeautifulSoup
import requests
import json
import html2text
class Group:
     
    def __init__(self, request_client):
        self._request = request_client.request
        
    
    async def groupSearch(self, name, show):
        url = f'https://www.roblox.com/search/groups/list-json?keyword={name}&maxRows={show}&startRow=0'
        results = json.loads(await self._request(url=url, method='GET'))['GroupSearchResults']
        return results

    async def getGroup(self, id, login=False):
        url = f'https://groups.roblox.com/v1/groups/{id}'
        results = json.loads(await self._request(url=url, method='GET'))
        return results
    
    async def getGroupRoles(self, id, login=False):
        url = f'https://groups.roblox.com/v1/groups/{id}/roles'
        results = json.loads(await self._request(url=url, method="GET"))
        return results
    
    async def groupPayout(self, groupid, userid, amount):
        url = f'https://groups.roblox.com/v1/groups/{groupid}/payouts'
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
        results = await self._request(url=url, method='POST', data=json.dumps(payout_data))
        return json.loads(results)

    async def postShout(self, groupid, message):
        url = f'https://groups.roblox.com/v1/groups/{groupid}/status'
        data = {
            'message': message
        }
        r = await self._request(url=url, method='PATCH', data=json.dumps(data))
        return r
    
    async def getWall(self, groupid):
        url = f'https://groups.roblox.com/v2/groups/{groupid}/wall/posts?limit=10'
        r = await self._request(url=url)
        return r

    async def getRoleInGroup(self, groupid, id):
        url = 'https://www.roblox.com/Game/LuaWebService/HandleSocialRequest.ashx?method=GetGroupRole&playerid=' + id + '&groupId=' + groupid
        r = await self._request(url=url)
        return json.loads(r)

    async def setRank(self, groupid, roleid, targetid):
        url = f'https://www.roblox.com/groups/api/change-member-rank?groupId={groupid}&newRoleSetId={roleid}&targetUserId={targetid}'
        r = await self._request(url=url, method='POST')
        return json.loads(r)

    async def promote(self, groupid, id):
        found_role = None
        roles = await self.getGroupRoles(groupid)['roles']
        user_role = await self.getRoleInGroup(groupid, id)
        for i in range(len(roles)):
            role = roles[i]
            if role['name'] == user_role:
                found_role = i
        if found_role is None:
            return {'ranked': False, 'reason': 'User not in group'}
        old_role_info = roles[int(found_role)]
        new_role_info = roles[int(found_role) + 1]
        r = await self.setRank(groupid, new_role_info['id'])
        if r['success'] is True:
            return {
                'ranked': True,
                'reason': '',
                'oldRole': old_role_info,
                'newRole': new_role_info
            }
        else:
            return {
                'ranked': False,
                'reason': 'Failed to rank member. Role too high'
            }

    async def demote(self, groupid, id):
        found_role = None
        roles = await self.getGroupRoles(groupid)['roles']
        user_role = await self.getRoleInGroup(groupid, id)
        for i in range(len(roles)):
            role = roles[i]
            if role['name'] == user_role:
                found_role = i
        if found_role is None:
            return {'ranked': False, 'reason': 'User not in group'}
        old_role_info = roles[int(found_role)]
        new_role_info = roles[int(found_role) - 1]
        r = await self.setRank(groupid, new_role_info['id'])
        if r['success'] is True:
            return {
                'ranked': True,
                'reason': '',
                'oldRole': old_role_info,
                'newRole': new_role_info
            }
        else:
            return {
                'ranked': False,
                'reason': 'Failed to rank member. Role too high'
            }




