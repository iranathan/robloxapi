from .request import request
from bs4 import BeautifulSoup
import requests
from .xcsrf import get_xcsrf
import json
class User:
     
    def __init__(self, cookie=str(), id=str()):
        self.cookie = None
        self.request = request(cookie).request
        self.xcsrf = get_xcsrf()
    
    #/users/get-by-username?username={id}
    def IdByUsername(self, username):
        r = self.request(url='http://api.roblox.com/users/get-by-username?username=' + username)
        return json.loads(r)
    #/users/{id}
    def UsernameById(self, id):
        r = self.request(url='http://api.roblox.com/users/' + id)
        return r
    
    
    def getProfile(self, id):
        url = 'https://www.roblox.com/users/' + str(id) + '/profile'
        r = self.request(url=url)
        soup = BeautifulSoup(r, 'html.parser')
        username = soup.find('h2').getText()
        avatar = str(soup.find('img').get('src'))
        blurb = soup.find('span', {'class': 'profile-about-content-text linkify'}).getText()
        status_req = self.request(url='https://www.roblox.com/users/profile/profileheader-json?userId=' + id)
        data = json.loads(status_req)
        status = data['UserStatus']
        follow_count = data['FollowersCount']
        Following_count = data['FollowingsCount'] 
        FriendsCount = data['FriendsCount']
        online_status = soup.find('span', {'class': 'avatar-status online profile-avatar-status icon-online'})
        playing_status = soup.find('span', {'class': 'avatar-status game icon-game profile-avatar-status'})
        get_status = ''
        if online_status:
            get_status = 'Browsing website'
        if playing_status:
            get_status = 'Playing a game'
        if not online_status and not playing_status:
            get_status = 'Offline'
      

        #bc check
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
        bc_img = str('https://www.roblox.com/Thumbs/BCOverlay.ashx?username=' + username)
        badge_url = 'https://www.roblox.com/badges/roblox?userId={}&imgWidth=110&imgHeight=110&imgFormat=png'.format(id)
        badge_data = self.request(url=badge_ur)
        Profile = {}
        Profile['username'] = username
        Profile['id'] = id
        Profile['avatar_url'] = avatar
        Profile['blurb'] = blurb
        Profile['status'] = status
        Profile['bc'] = {
            'type': bc,
            'image_url': bc_img
        }
        Profile['Activity']: get_status
        Profile['count'] = {
            'FollowersCount': follow_count,
            'FollowingsCount': Following_count,
            'FriendsCount': FriendsCount
        }
        Profile['badges'] = badge_data['RobloxBadges']
        return Profile

    #Requires auth:


    #https://www.roblox.com/messages/send
    def send_message(self, receiver_id, subject, body):
        data = {
            'body': body,
            'recipientid': receiver_id,
            'subject': subject
        }

        r = self.request(method='POST', url='https://www.roblox.com/messages/send', data=data)
        return json.loads(res.text)

    def block_user(self, id):
        url = 'https://www.roblox.com/userblock/blockuser'
        data = {
            'blockeeId': id
        }
        res = self.request(url=url, data=data)
        return json.loads(res)

    #https://www.roblox.com/userblock/unblockuser
    def unblock_user(self, id):
        url = 'https://www.roblox.com/userblock/unblockuser'
        data = {
            'blockeeId': id
        }
        res = self.request(url=url, data=data)
        return json.loads(res)
   
