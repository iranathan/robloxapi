from .utils.classes import *


class User:
    def __init__(self, request, roblox_id, roblox_name):
        self.request = request
        self.id = roblox_id
        self.name = roblox_name

    async def change_status(self, status: str) -> int:
        data = {'status': str(status)}
        r = await self.request.request(url='https://www.roblox.com/home/updatestatus', method='POST', data=json.dumps(data))
        return r.status_code

    async def send_message(self, recipient_id, subject, body) -> dict:
        data = {
            'recipientid': recipient_id,
            'subject': subject,
            'body': body
        }
        r = await self.request.request(url='https://www.roblox.com/messages/send', method='POST', data=json.dumps(data))
        return Message(recipient_id, subject, message, r.json()['success'])