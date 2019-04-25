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
        url = 'https://www.roblox.com/users/' + str(id) + '/profile'
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
        badge_data = Request(badge_url, parse=True)
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
        print(r.headers['X-CSRF-TOKEN'])
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

    def reportUser(self, id, tag, message):
        if self.cookie is not False:
            url = f'https://web.roblox.com/abusereport/userprofile?id={str(id)}&redirecturl=https%3a%2f%2fweb.roblox.com%2fusers%2f{str(id)}%2fprofile'
            cookies = {
                '.ROBLOSECURITY': self.cookie
            }
            headers = {
                'X-CSRF-TOKEN': get_xcsrf(),
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:66.0) Gecko/20100101 Firefox/66.0'
            }
            data = {
                'id': id,
                'RedirectUrl': f'https://web.roblox.com/users/{str(id)}/profile',
                'Comment': message,
                'PartyGuid': '',
                'ConversationId': '', #what does roblox want with those 2 things lol
                'ReportCategory': int(tag)
            }
            data = json.dumps(data)
            r = requests.post(url, data=data, headers=headers, cookies=cookies)
            return r.status_code
            #1 = Inappropriate Language - Profanity & Adult Content
            #2 = Asking for or Giving Priver Information
            #3 = Bullying, Harassment, Hate Speech
            #4 = Dating (wtf)
            #5 = Exploiting, Cheating, Spamming
            #6 = Account Theft - Phishing, Hacking, Trading
            #7 = Inappropriate Content - Place, Image, Model
            #8 = Real Life Threats & Suicide Threats
            #9 = Other Rule violation

        
             
            
            
        
    
        


        
        




    

    



        

