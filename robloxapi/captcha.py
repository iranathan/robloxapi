import httpx


class Captcha2:
    def __init__(self, token):
        self.requests = httpx.AsyncClient()
        self.token = token
        self.public_key = '9F35E182-C93C-EBCC-A31D-CF8ED317B996'

    async def make_task(self):
        url = f'https://2captcha.com/in.php?key={self.token}&method=funcaptcha&publickey={self.public_key}&pageurl=https://roblox.com/login&json=1' # json = 1
        r = await self.requests.post(url)
        return r.json()

    async def fetch_task(self, taskid):
        url = f'https://2captcha.com/res.php?key={self.token}&action=get&id={taskid}&json=1'
        r = await self.requests.get(url)
        return r.json()
