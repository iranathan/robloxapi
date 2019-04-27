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

    def getGroup(self, id, login=False):
        url = f'https://groups.roblox.com/v1/groups/{str(id)}'
        results = json.loads(self._request(url=url, method='GET'))
        return results
    
    def getGroupRoles(self, id, login=False):
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
      
    def postShout(self, groupid, message):
        url = f'https://groups.roblox.com/v1/groups/{str(groupid)}/status'
        data = {
            'message': message
        }
        print(data)
        r = self._request(url=url, method='PATCH', data=json.dumps(data))
        return r
