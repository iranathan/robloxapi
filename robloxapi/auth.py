import json


class Auth:
    """
    A holder for some authentication functions.
    """
    def __init__(self, request):
        """
        :param request: Used to send requests
        """
        self.request = request
        self.pkey = "9F35E182-C93C-EBCC-A31D-CF8ED317B996"
        self.bda = "W3sia2V5IjoiYXBpX3R5cGUiLCJ2YWx1ZSI6ImpzIn0seyJrZXkiOiJwIiwidmFsdWUiOjF9LHsia2V5IjoiZiIsInZhbHVlIjoiMWI1YmI1MTY4ZWRmMDcyZWU1OTFiOTNkMzgwOGUwMDUifSx7ImtleSI6Im4iLCJ2YWx1ZSI6Ik1UVTNPRFkyTmpReU9RPT0ifSx7ImtleSI6IndoIiwidmFsdWUiOiJmYWIxNDhlZmQyMzhhYWU2Zjg0MGRjOWI5MWVjYmEwMXwyMjUwMjc1ZjE1M2JhMzQwMGEzYjBlOTkzMTllZjRlNyJ9LHsia2V5IjoiZmUiLCJ2YWx1ZSI6WyJETlQ6dW5zcGVjaWZpZWQiLCJMOmVuLVVTIiwiRDoyNCIsIlBSOjIuNjA4Njk1NjUyMTczOTEzIiwiUzoxOTYzLDExMDQiLCJBUzoxOTYzLDEwMTgiLCJUTzotNjAiLCJTUzp0cnVlIiwiTFM6dHJ1ZSIsIklEQjp0cnVlIiwiQjpmYWxzZSIsIk9EQjpmYWxzZSIsIkNQVUM6dW5rbm93biIsIlBLOk1hY0ludGVsIiwiQ0ZQOjExMDQ1MjEyODUiLCJGUjpmYWxzZSIsIkZPUzpmYWxzZSIsIkZCOmZhbHNlIiwiSlNGOkFuZGFsZSBNb25vLEFyaWFsLEFyaWFsIEJsYWNrLEFyaWFsIEhlYnJldyxBcmlhbCBOYXJyb3csQXJpYWwgUm91bmRlZCBNVCBCb2xkLEFyaWFsIFVuaWNvZGUgTVMsQ29taWMgU2FucyBNUyxDb3VyaWVyLENvdXJpZXIgTmV3LEdlbmV2YSxHZW9yZ2lhLEhlbHZldGljYSxIZWx2ZXRpY2EgTmV1ZSxJbXBhY3QsTFVDSURBIEdSQU5ERSxNaWNyb3NvZnQgU2FucyBTZXJpZixNb25hY28sUGFsYXRpbm8sVGFob21hLFRpbWVzLFRpbWVzIE5ldyBSb21hbixUcmVidWNoZXQgTVMsVmVyZGFuYSxXaW5nZGluZ3MsV2luZ2RpbmdzIDIsV2luZ2RpbmdzIDMiLCJQOiIsIlQ6MCxmYWxzZSxmYWxzZSIsIkg6NCIsIlNXRjpmYWxzZSJdfSx7ImtleSI6ImNzIiwidmFsdWUiOjF9LHsia2V5IjoianNiZCIsInZhbHVlIjoie1wiSExcIjoxLFwiTkNFXCI6dHJ1ZSxcIkRNVE9cIjoxLFwiRE9UT1wiOjF9In1d"
        self.user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:66.0) Gecko/20100101 Firefox/66.0"

    async def login(self, username: str, password: str, token=None) -> tuple:
        """
        Used to login to roblox.
        :param username: The username to login with
        :param password: The psasword to login with
        :param token: The valid funcaptcha token to login with
        :return: Tuple with the status & cookies
        """
        data = {
            "ctype": "Username",
            "cvalue": username,
            "password": password,
            "captchaToken": token,
            "captchaProvider": "PROVIDER_ARKOSE_LABS"
        }
        r = await self.request.request(url="https://auth.roblox.com/v2/login", method="POST", noerror=True, data=json.dumps(data))
        return r.status_code, r.cookies


class Captcha:
    """
    A holder for some 2captcha functions
    """
    def __init__(self, request, key, pkey="9F35E182-C93C-EBCC-A31D-CF8ED317B996"):
        """
        :param request: Used to send requests
        :param key: 2captcha token
        :param pkey:
        """
        self.request = request
        self.key = key
        self.pkey = pkey

    async def create_task(self) -> tuple:
        """
        Created a 2captcha task
        :return: Json & StatusCode
        """
        r = await self.request.request(url=f'https://2captcha.com/in.php?key={self.key}&method=funcaptcha&publickey={self.pkey}&pageurl=https://roblox.com/login&json=1', method="POST")
        return r.json(), r.status_code

    async def check_task(self, task_id: int) -> tuple:
        """
        Checks a funcapcha
        :param task_id: The id of the task
        :return: Json & StatusCode
        """
        r = await self.request.request(url=f'https://2captcha.com/res.php?key={self.key}&action=get&id={task_id}&json=1', method="GET")
        return r.json(), r.status_code
