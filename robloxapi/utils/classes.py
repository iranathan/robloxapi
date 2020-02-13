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


class Limited:
    def __init__(self, limited_id, serial_number, user_asset_id, average_price):
        self.id = limited_id
        self.serial_number = serial_number
        self.user_asset_id = user_asset_id
        self.average_price = average_price
        self.original_price = original_price

