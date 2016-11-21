import os
import logging

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
        self.log = logging.getLogger(__name__)

    def register(self, url, methods, endpoint, plugin, context=None, name=None, description=None, ):

        if context is None and self.app.web.contexts.default_context is None:
            self.log.warning("Context not given and no default context is available. Basic context will be created")
            basic_context = self.app.web.contexts.register("basic",
                                                           os.path.join(self.app.path, "template"),
                                                           os.path.join(self.app.path, "static"),
                                                           "/",
                                                           "basic context, which was created automatically due the "
                                                           "miss of an available context during first route "
                                                           "registration.",
                                                           None)

            context = basic_context.name

        if context is None:
            context = self.app.web.contexts.default_context.name

        if name not in self._routes.keys():
            self._routes[name] = Route(url, methods, endpoint, context, name, description, plugin)

            for name, provider in self.app.web.providers.get().items():
                provider.instance.register_route(url, methods, endpoint, context)

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
