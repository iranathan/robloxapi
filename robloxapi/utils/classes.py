class Role:
    """
    Represents a role.
    """
    def __init__(self, role_id: int, role_name: str, rank=None, members=None):
        """
        :param role_id: The roles id
        :param role_name: The roles name
        :param rank: The roles rank (255, 254, etc)
        :param members: How many users have the role
        """
        self.id = role_id
        self.name = role_name
        self.rank = rank
        self.member_count = members


class Shout:
    """
    Represents a shout
    """
    def __init__(self, message: str, poster_name: str, poster_id: int, created: str, updated: str):
        """
        :param message: What the shout says
        :param poster_name: The authors name
        :param poster_id: The authors id
        :param created: When the post was created
        :param updated: When the shout was updated
        """
        self.message = message
        self.owner = {
            'name': poster_name,
            'id': poster_id
        }
        self.created = created
        self.updated = updated


class Message:
    """
    Represents a roblox message
    """
    def __init__(self, recipient_id: int, subject: str, message: str, success: bool):
        """
        :param recipient_id: The id of the recipient
        :param subject: The subject
        :param message: The message
        :param success: If it succeeded
        """
        self.recipient_id = recipient_id
        self.subject = subject
        self.message = message
        self.success = success


class Reseller:
    """
    Represents a user reselling a limited
    """
    def __init__(self, price, roblox_name, roblox_id, serial_number):
        """
        :param price: The price the user is reselling it for
        :param roblox_name: The name of the reseller
        :param roblox_id: The id of the reseller
        :param serial_number: The serial number of the limited
        """
        self.price = price
        self.name = roblox_name,
        self.id = roblox_id
        self.serial_number = serial_number


class WallPost:
    """
    Represents a wall post in a group.
    """
    def __init__(self, content, author):
        """
        :param content: contents of the message
        :param author: the author of the message
        """
        self.content = content
        self.author = author


class Action:
    """
    Represents an audit log action.
    """
    def __init__(self, action, actor, description, target=None):
        """
        :param action: What the action was
        :param actor: Who did the action
        :param description: What changed
        """
        self.action = action
        self.actor = actor
        self.description = description
        self.target = target
