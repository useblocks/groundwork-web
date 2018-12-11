import os
import logging

from groundwork.util import gw_get


class RouteManagerPlugin:
    def __init__(self, plugin):
        self.plugin = plugin
        self.log = plugin.log
        self.app = plugin.app

    def register(self, url, methods, endpoint=None, context=None, name=None, description=None, parameters=None):
        return self.app.web.routes.register(url, methods, self.plugin, endpoint, context, name, description, parameters)


class RouteManagerApplication:
    def __init__(self, app):
        self._routes = {}
        self.app = app
        self.log = logging.getLogger(__name__)
        self.blueprints = {}

    def register(self, url, methods, plugin, endpoint=None, context=None, name=None, description=None, parameters=None):

        if endpoint is not None and context is None and self.app.web.contexts.default_context is None:
            self.log.warning("Context not given and no default context is available. Basic context will be created")
            basic_context = self.app.web.contexts.register("basic",
                                                           os.path.join(self.app.path, "template"),
                                                           os.path.join(self.app.path, "static"),
                                                           "/",
                                                           "basic context, which was created automatically due the "
                                                           "miss of an available context during first route "
                                                           "registration.",
                                                           plugin)
            context = basic_context.name

        if context is None:
            context_obj = self.app.web.contexts.default_context
        else:
            context_obj = self.app.web.contexts.get(context)

        if name is None:
            name = endpoint

        if name not in self._routes.keys():
            self._routes[name] = Route(url, methods, context_obj, name, description, self.app,
                                       endpoint, plugin, parameters)

    def get(self, name=None, plugin=None):
        return gw_get(self._routes, name, plugin)


class Route:
    """
    """

    def __init__(self, url, methods, context, name, description, app, endpoint=None, plugin=None, parameters=None):
        self.url = url
        self.methods = methods
        self.endpoint = endpoint
        self.context = context
        self.name = name
        self.description = description
        self.plugin = plugin
        self.app = app
        self.parameters = parameters
        if self.parameters is None:
            self.parameters = {}
        self.log = logging.getLogger(__name__)

        if endpoint is not None:
            blueprint = self.context.blueprint
            blueprint.add_url_rule(url, methods=methods, endpoint=endpoint.__name__, view_func=endpoint)
            # We have to (re-)register our blueprint to activate the route
            self.app.web.flask.register_blueprint(blueprint)

        self.log.info("Route registered:  %s for context %s (%s)" % (self.url, self.context.name,
                                                                     self.context.url_prefix))
