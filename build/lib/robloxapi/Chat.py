import json


class Chat:
    def __init__(self, request_client):
        self._request = request_client.request
        self.base_url = 'https://chat.roblox.com/v2/'
    
    def getNewMessagesCount(self):
        url = self.base_url + 'get-unread-conversation-count'
        return json.loads(self._request(url=url))['count']

    def getNewMessages(self):
        count = self.getNewMessagesCount()
        url = self.base_url + 'get-user-conversations?pageNumber=1&pageSize=30'
        res = json.loads(self._request(url=url))
        message = []
        for i in list(range(len(res))):
            message.append(res[i])
            if i == count: break
        return message

    def startTyping(self, messageId, typing=True):
        url = self.base_url + 'update-user-typing-status'
        data = json.dumps({
            'conversationId': messageId,
            'isTyping': typing
        })
        r = self._request(url=url, data=data, method='POST')
        return json.loads(r)

    def stopTyping(self, messageId):
        return self.startTyping(messageId, typing=False)
    
    def sendMessage(self, messageId, content):
        url = self.base_url + 'send-message'
        data = json.dumps({
            'conversationId': messageId,
            'message': content
        })
        r = json.loads(self._request(url=url, method='POST', data=data))
        return {
            'timestamp': r['sent'],
            'freedomOfSpeechViolated': r['filteredForReceivers'],
            'content': content
        }

    def createGroup(self, userIds: list):
        url = self.base_url + 'start-group-conversation'
        data = json.dumps({
            'participantUserIds': userIds
        })
        r = json.loads(self._request(url=url, method='POST', data=data))['conversation']
        return {
            'id': r['id'],
            'title': r['title'],
            'members': r['participants']
        }