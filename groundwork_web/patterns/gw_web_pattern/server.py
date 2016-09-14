class ServerManagerPlugin:

    def __init__(self, plugin):
        self.plugin = plugin
        self.log = plugin.log
        self.app = plugin.app

    def register(self, name, description):
        return self.app.web.server.register(name, description, self.plugin)


class ServerManagerApplication:
    def __init__(self, app):
        self._servers = {}
        self.app = app

    def register(self, name, description, plugin):
        if name not in self._servers.keys():
            self._servers[name] = Server(name, description, plugin)


class Server:
    def __init__(self, name, start, description, plugin):
        self.name = name
        self.start = start
        self.description = description
        self.plugin = plugin
