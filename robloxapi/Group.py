from bs4 import BeautifulSoup
import requests
from .xcsrf import get_xcsrf
import json
class Group:
     
    def __init__(self, request_client):
        self._request = request_client.request
        
    
    def groupSearch(self, name, show):
        url = f'https://www.roblox.com/search/groups/list-json?keyword={str(name)}&maxRows={str(show)}&startRow=0'
        results = json.loads(self._request(url=url, method='GET'))['GroupSearchResults']  
        return results

    def getGroup(self, id):
        url = f'https://groups.roblox.com/v1/groups/{str(id)}'
        results = json.loads(self._request(url=url, method='GET'))
        return results
    
    def getGroupRoles(self, id):
        url = f'https://groups.roblox.com/v1/groups/{str(id)}/roles'
        results = json.loads(self._request(url=url, method="GET"))
        return results
    
    def groupPayout(self, groupid, userid, amount):
        url = f'https://groups.roblox.com/v1/groups/{str(groupid)}/payouts'
        payout_data = {
            'PayoutType': 'FixedAmount',
            'Recipients': [
                    {
                        'recipientId': id,
                        'recipientType': 'User',
                        'amount': amount,
                    }
                ]
            }
        results = self._request(url=url, method='POST', data=json.dumps(payout_data))
        return results
    
    def playerRankInGroup(self, groupid, id):
        url = 'https://www.roblox.com/Game/LuaWebService/HandleSocialRequest.ashx?method=GetGroupRole&playerid=' + str(id) + '&groupId=' + groupid
        r = self._request(url=url, method='GET')
        return r

      
    def postShout(self, groupid, message):
        url = f'https://groups.roblox.com/v1/groups/{str(groupid)}/status'
        data = {
            'message': message
        }
        print(data)
        r = self._request(url=url, method='PATCH', data=json.dumps(data))
        return r
     
    def setRank(self, groupid, roleid, targetid):
        url = f'https://www.roblox.com/groups/api/change-member-rank?groupId={groupid}&newRoleSetId={roleid}&targetUserId={targetid}'
        r = self._request(url=url, method='POST')
        return json.loads(r)
    
    def promote(self, groupid, targetid):
        cRole = None
        roles = self.getGroupRoles(groupid)
        roles = roles['roles']

        user_role = self.playerRankInGroup(groupid, targetid)
        for i in range(len(roles)):
            role = roles[int(i)]
            role_name = role['name']
            if role_name in user_role: 
                cRole = i
                print(cRole)
        if not cRole:
            raise Exception('Can\' find user: ' + targetid)
            return None
        role_id = roles[int(cRole)]
        return role_id


                


