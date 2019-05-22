import json


def unpack_json(json):
    try:
        return json.loads(json)
    except Exception as e:
        return json