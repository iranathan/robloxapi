class User:
    def __init__(self, request):
        self.request = request

    async def id_by_username(self, username) -> int:
        r = await self.request.request(url=f'http://api.roblox.com/users/get-by-username?username={username}', method='GET')
        return r.json().get('Id')

    async def username_by_id(self, rbx_id) -> str:
        r = await self.request.request(url=f'http://api.roblox.com/users/{rbx_id}', method='GET')
        return r.json().get('Username')

