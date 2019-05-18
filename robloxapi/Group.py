from bs4 import BeautifulSoup
import requests
import json
import html2text
class Group:
     
    def __init__(self, request_client):
        self._request = request_client.request
        
    
    def groupSearch(self, name, show):
        url = f'https://www.roblox.com/search/groups/list-json?keyword={name}&maxRows={show}&startRow=0'
        results = json.loads(self._request(url=url, method='GET'))['GroupSearchResults']  
        return results

    def getGroup(self, id, login=False):
        url = f'https://groups.roblox.com/v1/groups/{id}'
        results = json.loads(self._request(url=url, method='GET'))
        return results
    
    def getGroupRoles(self, id, login=False):
        url = f'https://groups.roblox.com/v1/groups/{id}/roles'
        results = json.loads(self._request(url=url, method="GET"))
        return results
    
    def groupPayout(self, groupid, userid, amount):
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
        results = self._request(url=url, method='POST', data=json.dumps(payout_data))
        return results
    
    def getAuditLogs(self, groupid):
        url = f'https://www.roblox.com/Groups/Audit.aspx?groupid={groupid}'
        r = self._request(url=url, method='GET')
        soup = BeautifulSoup(r, 'html.parser')
        found = soup.find('div', {'id': 'AuditPage'})
        allAudit = []
        for message in found.find_all('tr', {'class': 'datarow'}):
            print(type(message))
            if message is not None:
                description = str(message).split('<td class="Description">')[1]
                print(html2text.html2text(description))
           


    def postShout(self, groupid, message):
        url = f'https://groups.roblox.com/v1/groups/{groupid}/status'
        data = {
            'message': message
        }
        r = self._request(url=url, method='PATCH', data=json.dumps(data))
        return r
    
    def getWall(self, groupid):
        url = f'https://groups.roblox.com/v2/groups/{groupid}/wall/posts?limit=10'
        r = self._request(url=url)
        return r

    def getRoleInGroup(self, groupid, id):
        url = 'https://www.roblox.com/Game/LuaWebService/HandleSocialRequest.ashx?method=GetGroupRole&playerid=' + id + '&groupId=' + groupid
        r = self._request(url=url)
        return json.loads(r)

    def setRank(self, groupid, roleid, targetid):
        url = f'https://www.roblox.com/groups/api/change-member-rank?groupId={groupid}&newRoleSetId={roleid}&targetUserId={targetid}'
        r = self._request(url=url, method='POST')
        return json.loads(r)

    def promote(self, groupid, id):
        found_role = None
        roles = self.getGroupRoles(groupid)['roles']
        user_role = self.getRoleInGroup(groupid, id)
        for i in range(len(roles)):
            role = roles[i]
            if role['name'] == user_role:
                found_role = i
        if found_role is None:
            return {'ranked': False, 'reason': 'User not in group'}
        old_role_info = roles[int(found_role)]
        new_role_info = roles[int(found_role) + 1]
        r = self.setRank(groupid, new_role_info['id'])
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

    def demote(self, groupid, id):
        found_role = None
        roles = self.getGroupRoles(groupid)['roles']
        user_role = self.getRoleInGroup(groupid, id)
        for i in range(len(roles)):
            role = roles[i]
            if role['name'] == user_role:
                found_role = i
        if found_role is None:
            return {'ranked': False, 'reason': 'User not in group'}
        old_role_info = roles[int(found_role)]
        new_role_info = roles[int(found_role) - 1]
        r = self.setRank(groupid, new_role_info['id'])
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




