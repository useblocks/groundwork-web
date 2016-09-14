class ProviderManagerPlugin:

    def __init__(self, plugin):
        self.plugin = plugin
        self.log = plugin.log
        self.app = plugin.app

    def register(self, name, instance, description):
        return self.app.web.providers.register(name, instance, description, self.plugin)


class ProviderManagerApplication:
    def __init__(self, app):
        self._providers = {}
        self.app = app

    def register(self, name, instance, description, plugin):
        if name not in self._providers.keys():
            self._providers[name] = Provider(name, instance, description, plugin)


class Provider:
    def __init__(self, name, instance, description, plugin):
        self.name = name
        self.instance = instance
        self.description = description
        self.plugin = plugin

