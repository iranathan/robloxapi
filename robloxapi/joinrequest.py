from .user import *
import json


class JoinRequest:
    def __init__(self, request, group_id, roblox_name, roblox_id):
        self.request = request
        self.id = group_id
        self.user = User(request, int(roblox_id), roblox_name)

    async def accept(self) -> int:
        r = await self.request.request(url=f"https://groups.roblox.com/v1/groups/{self.id}/join-requests/users/{self.user.id}", method="POST", chunk=True)
        return r.status_code

    async def decline(self) -> int:
        r = await self.request.request(url=f"https://groups.roblox.com/v1/groups/{self.id}/join-requests/users/{self.user.id}", method="DELETE", chunk=True)
        return r.status_code
