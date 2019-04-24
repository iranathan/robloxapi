import requests

data = {
    'username': 'TheGodPerson101_Pro',
    'password': 'monkeymonkey'
}

print(requests.post('https://www.roblox.com/MobileAPI/Login', data=data))