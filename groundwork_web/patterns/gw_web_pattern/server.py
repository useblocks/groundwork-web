from groundwork.util import gw_get


class ServerManagerPlugin():

    def __init__(self, plugin):
        self.plugin = plugin
        self.log = plugin.log
        self.app = plugin.app

    def register(self, name, function, description):
        return self.app.web.servers.register(name, function, description, self.plugin)

    def get(self, name=None):
        """
        Returns servers, which can be filtered by name.

        :param name: name of the server
        :type name: str
        :return: None, single server or dict of servers
        """
        return self.app.web.servers.get(name, self.plugin)


class ServerManagerApplication:
    def __init__(self, app):
        self._servers = {}
        self.app = app

    def register(self, name, function, description, plugin):
        if name not in self._servers.keys():
            self._servers[name] = Server(name, function, description, plugin)

    def get(self, name=None, plugin=None):
        """
        Returns servers, which can be filtered by name or plugin.

        :param name: name of the server
        :type name: str
        :param plugin: plugin name, which registers the servers
        :return: None, single server or dict of servers
        """
        return gw_get(self._servers, name, plugin)


class Server():
    def __init__(self, name, function, description, plugin):
        self.name = name
        self.function = function
        self.description = description
        self.plugin = plugin
