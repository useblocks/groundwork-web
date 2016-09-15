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
        self.default_context = None

    def register(self, name, template_folder, static_folder, url_prefix, description, plugin):
        if name not in self._contexts.keys():
            self._contexts[name] = Context(name, template_folder, static_folder, url_prefix, description, plugin)
            if name == self.app.config.get("DEFAULT_CONTEXT", None) or self.default_context is None:
                self.default_context = self._contexts[name]

        for name, provider in self.app.web.providers.get().items():
            provider.register_context()

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
    def __init__(self, name, template_folder, static_folder, url_prefix, description, plugin):
        self.name = name
        self.template_folder = template_folder
        self.static_folder = static_folder
        self.url_prefix = url_prefix
        self.description = description
        self.plugin = plugin
