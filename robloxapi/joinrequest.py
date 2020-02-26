from .user import *
import json


class JoinRequest:
    """
    Represents a join request
    """
    def __init__(self, request, group_id, roblox_name, roblox_id):
        """
        Created a join request
        :param request: Used to send requests
        :param group_id: The group id the request belongs to
        :param roblox_name: The name of the requester
        :param roblox_id: The id of the requester
        """
        self.request = request
        self.id = group_id
        self.user = User(request, int(roblox_id), roblox_name)

    async def accept(self) -> int:
        """
        Accepts the join request
        :return: StatusCode
        """
        r = await self.request.request(url=f"https://groups.roblox.com/v1/groups/{self.id}/join-requests/users/{self.user.id}", method="POST", chunk=True)
        return r.status_code

    async def decline(self) -> int:
        """
        Declines the join requests
        :return: StatusCode
        """
        r = await self.request.request(url=f"https://groups.roblox.com/v1/groups/{self.id}/join-requests/users/{self.user.id}", method="DELETE", chunk=True)
        return r.status_code
