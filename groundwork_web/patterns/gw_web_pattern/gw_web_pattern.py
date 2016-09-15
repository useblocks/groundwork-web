import logging
from groundwork.patterns import GwBasePattern

from groundwork_web.patterns.gw_web_pattern.provider import ProviderManagerApplication, ProviderManagerPlugin
from groundwork_web.patterns.gw_web_pattern.server import ServerManagerApplication, ServerManagerPlugin
from groundwork_web.patterns.gw_web_pattern.context import ContextManagerApplication, ContextManagerPlugin
from groundwork_web.patterns.gw_web_pattern.route import RouteManagerApplication, RouteManagerPlugin


class GwWebPattern(GwBasePattern):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not hasattr(self.app, "web"):
            self.app.web = WebApplication(self.app)

        #: Instance of :class:`~.WebPlugin`.
        #: Provides functions to manage web based objects
        self.web = WebPlugin(self)


class WebPlugin:
    def __init__(self, plugin):
        self.plugin = plugin
        self.app = plugin.app
        self.log = plugin.log
        self.providers = ProviderManagerPlugin(plugin)
        self.servers = ServerManagerPlugin(plugin)
        self.contexts = ContextManagerPlugin(plugin)
        self.routes = RouteManagerPlugin(plugin)


class WebApplication:
    def __init__(self, app):
        self.app = app
        self.log = logging.getLogger(__name__)
        self.providers = ProviderManagerApplication(app)
        self.servers = ServerManagerApplication(app)
        self.contexts = ContextManagerApplication(app)
        self.routes = RouteManagerApplication(app)


