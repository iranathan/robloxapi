from bs4 import BeautifulSoup
import json


class User:
    def __init__(self, request):
        self.request = request

    async def id_by_username(self, username) -> int:
        r = await self.request.request(url=f'http://api.roblox.com/users/get-by-username?username={username}', method='GET')
        return r.json().get('Id')

    async def username_by_id(self, rbx_id) -> str:
        r = await self.request.request(url=f'http://api.roblox.com/users/{rbx_id}', method='GET')
        return r.json().get('Username')

    async def search_user(self, keyword) -> list:
        r = await self.request.request(url=f'https://www.roblox.com/search/users/results?keyword={keyword}&maxRows=12&startIndex=0', method='GET')
        return r.json().get('UserSearchResults') or []

    async def get_profile(self, rbx_id) -> dict:
        r = await self.request.request(url=f'https://www.roblox.com/users/{rbx_id}/profile', method='GET')
        soup = BeautifulSoup(r.text, 'html.parser')
        username = soup.find('h2').text
        blurb = soup.find('span', {'class': 'profile-about-content-text linkify'}).getText()
        avatar = soup.find('img', {'alt': username})['src']
        bc = 'NBC'
        getBc = soup.find('span', {'class': 'icon-bc'})
        getTbc = soup.find('span', {'class': 'icon-tbc'})
        getObc = soup.find('span', {'class': 'icon-obc'})
        if getBc is not None:
            bc = 'BC'
        if getTbc is not None:
            bc = 'TBC'
        if getObc is not None:
            bc = 'OBC'
        online_status = soup.find('span', {'class': 'avatar-status online profile-avatar-status icon-online'})
        playing_status = soup.find('span', {'class': 'avatar-status game icon-game profile-avatar-status'})
        get_status = ''
        if online_status:
            get_status = 'Browsing website'
        if playing_status:
            get_status = 'Playing a game'
        if not online_status and not playing_status:
            get_status = 'Offline'

        return {
            'username': username,
            'blurb': blurb,
            'avatar': avatar,
            'bc': bc,
            'presence': get_status
        }

    async def update_status(self, status) -> dict:
        data = {'status': str(status)}
        r = await self.request.request(url='https://www.roblox.com/home/updatestatus', method='POST', data=json.dumps(data))
        return r.json()

    async def block_user(self, rbx_id) -> dict:
        data = {'blockeeId': rbx_id}
        r = await self.request.request(url='https://www.roblox.com/userblock/blockuser', method='POST', data=json.dumps(data))
        return r.json()

    async def unblock_user(self, rbx_id) -> dict:
        data = {'blockeeId': rbx_id}
        r = await self.request.request(url='https://www.roblox.com/userblock/unblockuser', method='POST', data=json.dumps(data))
        return r.json()

    async def add_friend(self, rbx_id) -> dict:
        data = {'targetUserID': int(Userid)}
        r = await self.request.request(url='https://www.roblox.com/api/friends/sendfriendrequest', method='POST', data=json.dumps(data))
        return r

    async def send_message(self, recipientid, subject, body) -> dict:
        data = {
            'recipientid': recipientid,
            'subject': subject,
            'body': body
        }
        r = await self.request.request(url='https://www.roblox.com/messages/send', method='POST', data=json.dumps(data))
        return r.json()
