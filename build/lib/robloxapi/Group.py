from bs4 import BeautifulSoup
import requests
import json
import html2text
import re
from .utils.Errors import AuthError
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
        return json.loads(results)

    def getJoinRequests(self, groupid):
        url = f'https://www.roblox.com/groups/{groupid}/joinrequests-html?pageNum=1'
        r = self._request(url=url, method='GET')
        soup = BeautifulSoup(r, 'html.parser')
        found = soup.find('tbody')
        tr = found.find_all('tr')
        del tr[-1]
        requests = []
        for request in tr:
            requests.append({
                'JoinId': request.find('span', {"class": "btn-control btn-control-medium accept-join-request"})['data-rbx-join-request'],
                'User': {
                    'AvatarPicture': request.td.span.img['src'],
                    'Username': request.find('a').text,
                    'Id': re.findall(r'\b\d+\b', request.find('a')['href']),
                    'ProfileLink': request.find('a')['href']
                }
            })
        return requests


    def postShout(self, groupid, message):
        url = f'https://groups.roblox.com/v1/groups/{groupid}/status'
        data = {
            'message': message
        }
        r = self._request(url=url, method='PATCH', data=json.dumps(data))
        return json.loads(r)
    
    def getAuditLog(self, groupid):
        logs = []
        url = f'https://www.roblox.com/Groups/Audit.aspx?groupid={groupid}'
        r = self._request(url=url, response=True)
        if r.url.find('/Groups/Group.aspx?gid=') != -1:
            raise AuthError('Unable to get audit log.')
        soup = BeautifulSoup(r.text, 'html.parser')
        for datarow in soup.find('table', {'class': 'AuditLogContainer'}).find_all('tr', {'class': 'datarow'}):
            date = datarow.td['class']
            username = datarow.find('span', {'class': 'username'}).text
            user_id = datarow.find('td', {'class': 'User'}).div['data-user-id']
            group_rank = datarow.find('td', {'class': 'Rank'}).span.text
            description = datarow.find('td', {'class': 'Description'}).get_text()
            logs.append({
                'date': date,
                'username': username,
                'userId': user_id,
                'groupRank': group_rank,
                'description': description
            })
        return logs

    def getWall(self, groupid):
        url = f'https://groups.roblox.com/v2/groups/{groupid}/wall/posts?limit=10'
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

