from bs4 import BeautifulSoup
import requests
from .xcsrf import get_xcsrf
import json
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
            user = message.find('tr', {'class': 'User'})
            username = user.span.getText()
            description = message.find('td', {'class': 'Description'})
            description_text = message.getText()
            audit_info = {
                'User': {
                    'username': username
                },
                'Description': description_text
            }
            allAudit.append(audit_info)
        return allAudit
           


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
