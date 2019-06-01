from threading import Timer
import json

class RepeatedTimer(object):
    def __init__(self, interval, function, *args, **kwargs):
        self._timer = None
        self.interval = interval
        self.function = function
        self.args = args
        self.kwargs = kwargs
        self.is_running = False
        self.start()

    def _run(self):
        self.is_running = False
        self.start()
        self.function(*self.args, **self.kwargs)

    def start(self):
        if not self.is_running:
            self._timer = Timer(self.interval, self._run)
            self._timer.start()
            self.is_running = True

    def stop(self):
        self._timer.cancel()
        self.is_running = False


class Event:
    def __init__(self, request, event, function, args=None, client=None):
        self.event = event
        self._request = request.request
        self.function = function
        self.catch = {}
        self.client = client
        if event == 'onShout':
            self.rt = RepeatedTimer(3, self.onShout, args)
        elif event == 'onAuditChange':
            self.rt = RepeatedTimer(3, self.onAuditChange, args)

    def onShout(self, id):
        url = f'https://groups.roblox.com/v1/groups/{id}'
        results = json.loads(self._request(url=url, method='GET'))
        if str(self.catch) == '{}': self.catch = results['shout']
        if results['shout'] == None: return
        if 'body' in self.catch:
            if self.catch['body'] == results['shout']['body']: return
            self.catch = results['shout']
            self.function(results['shout'])

    def onAuditChange(self, id):
        current_audit = self.client.Group.getAuditLog(id)
        catched = None
        if not catched: catched = current_audit
        log = []
        for i in list(range(len(current_audit))):
            try:
                catched[i]
            except IndexError:
                log.append(current_audit[i])
        if len(catched) < len(current_audit):
            self.function(log)




