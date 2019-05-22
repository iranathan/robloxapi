import json


def unpack_json(json):
    try:
        return json.loads(json)
    except Exception as e:
        return json

    
def is_num(s):
    try:
        int(s)
        return True
    except ValueError:
        return False
