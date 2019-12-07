class Role:
    def __init__(self, role_id, role_name, rank, members):
        self.id = role_id
        self.name = role_name
        self.rank = rank
        self.member_count = int(members)


class Shout:
    def __init__(self, message, poster_name, poster_id, created, updated):
        self.message = message
        self.owner = {
            'name': poster_name,
            'id': poster_id
        }
        self.created = created
        self.updated = updated


class Message:
    def __init__(self, recipient_id, subject, message, success):
        self.recipient_id = recipient_id
        self.subject = subject
        self.message = message
        self.success = success
