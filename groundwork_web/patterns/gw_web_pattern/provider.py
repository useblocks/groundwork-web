from groundwork.util import gw_get


class ProviderManagerPlugin:

    def __init__(self, plugin):
        self.plugin = plugin
        self.log = plugin.log
        self.app = plugin.app
        # self.default = plugin.app.web.providers.default

    def register(self, name, instance, description):
        return self.app.web.providers.register(name, instance, description, self.plugin)

    def render(self, *args, **kwargs):
        return self.app.web.providers.render(*args, **kwargs)


class ProviderManagerApplication:
    def __init__(self, app):
        self._providers = {}
        self.app = app
        self.default = None

    def register(self, name, instance, description, plugin):
        if name not in self._providers.keys():
            self._providers[name] = Provider(name, instance, description, plugin)
            self._load_context(self._providers[name])
            self._load_routes(self._providers[name])

        if name == self.app.config.get("DEFAULT_PROVIDER", None) or self.default is None:
            self.default = self._providers[name]

        return self._providers[name]

    def render(self, template, provider=None, **kwargs):
        if self.default is None:
            raise RuntimeError("No default provider is set")
        if provider is None:
            return self.default.instance.render(template, **kwargs)
        if provider not in self._providers.keys():
            raise NameError("Provider %s does not exist" % provider)

        return self._providers[provider].instance.render(template, **kwargs)

    def set_default_provider(self, name):
        if name not in self._providers.keys():
            raise NameError("Provider %s does not exist" % name)
        self.default = self._providers[name]

    def get(self, name=None, plugin=None):
        return gw_get(self._providers, name, plugin)

    def _load_routes(self, provider):
        if provider.instance is not None:
            for name, route in self.app.web.routes.get().items():
                provider.instance.register_route(route.url, route.methods, route.endpoint, route.context)

    def _load_context(self, provider):
        if provider.instance is not None:
            for name, context in self.app.web.contexts.get().items():
                provider.instance.register_context(context.name, context.template_folder,
                                                   context.static_folder, context.url_prefix)


class Provider:
    def __init__(self, name, instance, description, plugin):
        self.name = name

        if isinstance(instance, BaseProvider):
            self.instance = instance
        else:
            raise TypeError("instance must be of type BaseProvider, got %s instead" % str(type(instance)))

        self.description = description
        self.plugin = plugin


class BaseProvider:
    def __init__(self, instance=None):
        self.instance = instance
        self.request = None

    def register_route(self, url, methods, endpoint, context, *arg, **kwargs):
        pass

    def unregister_route(self, url, methods, context, *arg, **kwargs):
        pass

    def register_context(self, name, template_folder, static_folder, url_prefix, *arg, **kwargs):
        pass

    def unregister_context(self, name):
        pass

    def render(self, template, **kwargs):
        pass
