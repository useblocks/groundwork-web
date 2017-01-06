import logging
from flask import Blueprint

from groundwork.util import gw_get


class ContextManagerPlugin:
    def __init__(self, plugin):
        self.plugin = plugin
        self.log = plugin.log
        self.app = plugin.app

    def register(self, name, template_folder, static_folder, url_prefix, description):
        return self.app.web.contexts.register(name, template_folder, static_folder,
                                              url_prefix, description, self.plugin)


class ContextManagerApplication:
    def __init__(self, app):
        self._contexts = {}
        self.app = app
        self.log = logging.getLogger(__name__)
        self.default_context = None

    def register(self, name, template_folder, static_folder, url_prefix, description, plugin):
        if name not in self._contexts.keys():
            self._contexts[name] = Context(name, template_folder, static_folder, url_prefix, description, plugin,
                                           self.app)
            if name == self.app.config.get("DEFAULT_CONTEXT", None) or self.default_context is None:
                self.default_context = self._contexts[name]
        else:
            self.log.warning("Context %s already registered by %s" % (name, self._contexts[name].plugin.name))

        return self._contexts[name]

    def get(self, name=None, plugin=None):
        return gw_get(self._contexts, name, plugin)


class Context:
    """
    Contexts are used to collect common objects in a single place and make it easy for new web routes to reuse
    these objects.

    Common objects are:

     * A template folder
     * A static folder
     * A url_prefix
     * A static folder web route, which gets automatically calculated based on given context name

    They are similar to flask blueprint concept.
    """

    def __init__(self, name, template_folder, static_folder, url_prefix, description, plugin, app):
        self.name = name
        self.template_folder = template_folder
        self.static_folder = static_folder
        self.url_prefix = url_prefix
        self.static_url_path = "/static"
        self.description = description
        self.plugin = plugin
        self.app = app
        self.log = logging.getLogger(__name__)

        self.blueprint = Blueprint(name, __name__,
                                   url_prefix=url_prefix,
                                   subdomain=None,
                                   template_folder=template_folder,
                                   static_folder=static_folder,
                                   static_url_path=self.static_url_path)
        self.app.web.flask.register_blueprint(self.blueprint)

        self.log.debug("Context registered: %s (%s) for plugin %s" % (self.name, self.url_prefix, self.plugin.name))
