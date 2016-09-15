from groundwork.util import gw_get


class RouteManagerPlugin:

    def __init__(self, plugin):
        self.plugin = plugin
        self.log = plugin.log
        self.app = plugin.app

    def register(self, url, methods, endpoint, context=None, name=None, description=None):
        return self.app.web.routes.register(url, methods, endpoint, self.plugin, context, name, description)


class RouteManagerApplication:
    def __init__(self, app):
        self._routes = {}
        self.app = app

    def register(self, url, methods, endpoint, plugin, context=None, name=None, description=None,):
        if context is None and self.app.web.contexts.default_context is None:
            raise RuntimeError("Context not give and no default context is available.")

        if context is None:
            context = self.app.web.contexts.default_context.name

        if name not in self._routes.keys():
            self._routes[name] = Route(url, methods, endpoint, context, name, description, plugin)

            for provider in self.app.web.providers.get():
                provider.instance.register_route()

    def get(self, name=None, plugin=None):
        return gw_get(self._routes, name, plugin)


class Route:
    """
    """
    def __init__(self, url, methods, endpoint, context, name, description, plugin):
        self.url = url
        self.methods = methods
        self.endpoint = endpoint
        self.context = context
        self.name = name
        self.description = description
        self.plugin = plugin

