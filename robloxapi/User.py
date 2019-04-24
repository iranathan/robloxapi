from .request import Request
from bs4 import BeautifulSoup
import requests
from .xcsrf import get_xcsrf
import json
class User:
     
    def __init__(self, cookie=str(), id=str()):
        if cookie is None:
            self.cookie = False
            self.id = False
        self.cookie = cookie
        self.id = id
        self.xcsrf = get_xcsrf()
    
    #/users/get-by-username?username={id}
    def IdByUsername(self, username):
        r = Request('http://api.roblox.com/users/get-by-username?username=' + username, parse=True)
        return r
    #/users/{id}
    def UsernameById(self, id):
        r = Request('http://api.roblox.com/users/' + id, parse=True)
        return r
    
    
    def getProfile(self, id):
        url = 'https://www.roblox.com/users/' + id + '/profile'
        r = Request(url, parse=False)
        soup = BeautifulSoup(r, 'html.parser')
        username = soup.find('h2').getText()
        avatar = str(soup.find('img').get('src'))
        blurb = soup.find('span', {'class': 'profile-about-content-text linkify'}).getText()
        status_req = requests.get('https://www.roblox.com/users/profile/profileheader-json?userId=' + id)
        data = json.loads(status_req.text)
        status = data['UserStatus']
        follow_count = data['FollowersCount']
        Following_count = data['FollowingsCount'] 
        FriendsCount = data['FriendsCount']
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
        badge_data = Request(badge_url, parse=True)
        Profile = {}
        Profile['username'] = username
        Profile['id'] = id
        Profile['avatar_url'] = avatar
        Profile['blurb'] = blurb
        Profile['bc'] = {
            'type': bc,
            'image_url': bc_img
        }
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
        if self.cookie is False:
            raise Exception('Not logged in.')
            
        data = {
            'body': body,
            'recipientid': receiver_id,
            'subject': subject
        }
        cookies = {
            '.ROBLOSECURITY': self.cookie
        }
        headers = {
            'X-CSRF-TOKEN': get_xcsrf(),
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:66.0) Gecko/20100101 Firefox/66.0'
        }
        r = requests.post('https://www.roblox.com/messages/send', data=data, cookies=cookies, headers=headers)
        headers['X-CSRF-TOKEN'] = r.headers['X-CSRF-TOKEN']
        res = requests.post('https://www.roblox.com/messages/send', data=data, cookies=cookies, headers=headers)
        return res.text + ' ' + str(res.status_code)

    def block_user(self, id):
        if self.cookie is False:
            raise Exception('Not logged in.')
        url = 'https://www.roblox.com/userblock/blockuser'
        data = {
            'blockeeId': id
        }
        cookies = {
            '.ROBLOSECURITY': self.cookie
        }
        headers = {
            'X-CSRF-TOKEN': get_xcsrf(),
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:66.0) Gecko/20100101 Firefox/66.0'
        }
        res = requests.post(url, data=data, cookies=cookies, headers=headers)
        if res.status_code == 403:
            headers['X-CSRF-TOKEN'] = res.headers['X-CSRF-TOKEN']
            res = requests.post(url, data=data, cookies=cookies, headers=headers)
            if json.loads(res.text)['success'] is True:
                return json.loads(res.text)
        elif res.status_code != 403 and res.status_code != 200:
            print('Rython: Failed to block user')
            return False
        else:
            if json.loads(res.text)['success'] is True:
                return json.loads(res.text)
            else:
                print('Rython: Failed to block user')
                return False

    #https://www.roblox.com/userblock/unblockuser
    def unblock_user(self, id):
        if self.cookie is False:
            raise Exception('Not logged in.')
        url = 'https://www.roblox.com/userblock/unblockuser'
        data = {
            'blockeeId': id
        }
        cookies = {
            '.ROBLOSECURITY': self.cookie
        }
        headers = {
            'X-CSRF-TOKEN': get_xcsrf(),
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:66.0) Gecko/20100101 Firefox/66.0'
        }
        res = requests.post(url, data=data, cookies=cookies, headers=headers)
        if res.status_code == 403:
            headers['X-CSRF-TOKEN'] = res.headers['X-CSRF-TOKEN']
            res = requests.post(url, data=data, cookies=cookies, headers=headers)
            if json.loads(res.text)['success'] is True:
                return json.loads(res.text)
        elif res.status_code != 403 and res.status_code != 200:
            print('Rython: Failed to block user')
            return False
        else:
            if json.loads(res.text)['success'] is True:
                return json.loads(res.text)
            else:
                print('Rython: Failed to block user')
                return False
       

        
             
            
            
        
    
        


        
        




    

    



        

