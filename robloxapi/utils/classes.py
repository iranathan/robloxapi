class Role:
    def __init__(self, role_id: int, role_name: str, rank: int, members: int):
        self.id = role_id
        self.name = role_name
        self.rank = rank
        self.member_count = members


class Shout:
    def __init__(self, message: str, poster_name: str, poster_id: int, created: str, updated: str):
        self.message = message
        self.owner = {
            'name': poster_name,
            'id': poster_id
        }
        self.created = created
        self.updated = updated


class Message:
    def __init__(self, recipient_id: int, subject: str, message: str, success: bool):
        self.recipient_id = recipient_id
        self.subject = subject
        self.message = message
        self.success = success


class Reseller:
    def __init__(self, price, roblox_name, roblox_id, serial_number):
        self.price = price
        self.name = roblox_name,
        self.id = roblox_id
        self.serial_number = serial_number
