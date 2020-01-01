import json


class JoinRequest:
    def __init__(self, request, request_id, roblox_name, roblox_id, roblox_avatar):
        self.request = request
        self.request_id = request_id
        self.user = {
            'name': roblox_name,
            'id': roblox_id,
            'avatar': roblox_avatar
        }

    async def accept(self) -> int:
        data = {
            'groupJoinRequestId': self.request_id,
            'accept': True
        }
        r = await self.request.request(url=f'https://www.roblox.com/group/handle-join-request', data=json.dumps(data), method='POST')
        return r.status_code

    async def decline(self) -> int:
        data = {
            'groupJoinRequestId': self.request_id,
            'accept': False
        }
        r = await self.request.request(url=f'https://www.roblox.com/group/handle-join-request', data=json.dumps(data), method='POST')
        return r.status_code
