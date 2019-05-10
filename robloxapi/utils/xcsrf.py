import requests
def get_xcsrf():
    r = requests.post('https://www.roblox.com/favorite/toggle').headers
    return r['X-CSRF-TOKEN']
