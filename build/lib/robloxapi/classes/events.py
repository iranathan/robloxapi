class Events:

    def init(self, function):
        self.function = function

    def fire(self, **args):
        self.function(**args)