from bs4 import BeautifulSoup
import requests
import json
class User:
     
    def __init__(self, request_client):
        self.cookie = None
        self._request = request_client.request
    
    #/users/get-by-username?username={id}
    def IdByUsername(self, username):
        r = self._request(url='http://api.roblox.com/users/get-by-username?username=' + username)
        return json.loads(r)
    #/users/{id}
    def UsernameById(self, id):
        r = self._request(url='http://api.roblox.com/users/' + str(id))
        return r
    
    def searchUsers(self, keyword):
        if len(str(keyword)) > 3:
            url = f'https://www.roblox.com/search/users/results?keyword={ketword}&maxRows=12&startIndex=0'
    
    def getProfile(self, id):
        url = 'https://www.roblox.com/users/' + str(id) + '/profile'
        r = self._request(url=url)
        soup = BeautifulSoup(r, 'html.parser')
        username = soup.find('h2').getText()
        avatar = str(soup.find('img').get('src'))
        blurb = soup.find('span', {'class': 'profile-about-content-text linkify'}).getText()
        status_req = self._request(url='https://www.roblox.com/users/profile/profileheader-json?userId=' + id)
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
        badge_data = json.loads(self._request(url=badge_url))
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

    def get_self(self):
        url = 'https://www.roblox.com/game/GetCurrentUser.ashx'
        res = self._request(url=url, method="GET")
        return res
     
    def updateStatus(self, newStatus, facebook=False):
        url = 'https://www.roblox.com/home/updatestatus'
        data = {'status': str(newStatus)}
        if facebook is True:
            data['sendToFacebook'] = True
        data = json.dumps(data)
        r = self._request(url=url, method='POST', data=data)
    

    def blockUser(self, id):
        url = 'https://www.roblox.com/userblock/blockuser'
        data = json.dumps({'blockeeId': id})
        r = self._request(url=url, method='POST', data=data)
        return r
    
    def unblockUser(self, id):
        url = 'https://www.roblox.com/userblock/unblockuser'
        data = json.dumps({'blockeeId': id}) 
        r = self._request(url=data, method='POST', data=data)
        return r
    
    def addFriend(self, Userid):
        url = 'https://www.roblox.com/api/friends/sendfriendrequest'
        data = {
            'targetUserID': int(Userid)
        }
        r = self._request(url=url, data=json.dumps(data), method='POST')
        return r
   
    def removeFriend(self, Userid):
        url = 'https://www.roblox.com/api/friends/removefriend'
        data = {
            'targetUserID': int(Userid)
        }
        r = self._request(url=url, data=json.dumps(data), method='POST')
        return r

