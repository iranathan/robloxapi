class Group:

    def __init__(self, request, id):
        self.groupId = id
        self._requests = request.request

    def getGroup(self):
        url = f'https://groups.roblox.com/v1/groups/{self.groupId}'
        results = json.loads(self._request(url=url, method='GET'))
        return results

    def getGroupRoles(self):
        url = f'https://groups.roblox.com/v1/groups/{self.groupId}/roles'
        results = json.loads(self._request(url=url, method="GET"))
        return results

    def groupPayout(self, userid, amount):
        url = f'https://groups.roblox.com/v1/groups/{self.groupId}/payouts'
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

    def postShout(self, message):
        url = f'https://groups.roblox.com/v1/groups/{self.groupId}/status'
        data = {
            'message': message
        }
        r = self._request(url=url, method='PATCH', data=json.dumps(data))
        return r

    def getWall(self):
        url = f'https://groups.roblox.com/v2/groups/{self.groupId}/wall/posts?limit=10'
        r = self._request(url=url)
        return r