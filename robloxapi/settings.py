import json


class Settings:
    def __init__(self, request):
        self.requests = request

    async def description(self, value):
        data = {
            'description': value.replace(' ', '+')
        }
        r = await self.requests(method='POST', url='https://accountinformation.roblox.com/v1/description', data=json.dumps(data))
        return r.status_code == 200

    async def birthday(self, day, month, year):
        data = {
            'birthDay': day,
            'birthMonth': month,
            'birthYear': year
        }
        r = await self._request(url='https://accountinformation.roblox.com/v1/birthdate', method='POST', data=json.dumps(data))
        return r.status_code == 200

    async def gender(self, gender):
        data = {
            'gender': gender
        }
        r = await self._request(url='https://accountinformation.roblox.com/v1/description', method='POST', data=json.dumps(data))
        return r.status_code == 200
