import requests
from json import loads

def Request(url, parse=True):
    r = requests.get(url)
    if r.status_code is not 200:
        raise Exception('Ryblox: Error with url ' + url + ' Code: ' + str(r.status_code ))
    else:
        if parse is True:
            return loads(r.text)
        else:
            return r.text

def client_Request(url, parse=True, cookies=str()):
    r = requests.get(url, cookies=cookies)
    if parse is True:
        return json.loads(r.text)
    else:
        return r.text
        
   