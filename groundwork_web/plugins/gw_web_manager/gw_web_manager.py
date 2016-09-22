import os
from click import Argument, echo
from groundwork_web.patterns import GwWebPattern


class GwWebManager(GwWebPattern):
    def __init__(self, *args, **kwargs):
        self.name = kwargs.get("name", self.__class__.__name__)
        super().__init__(*args, **kwargs)

    def activate(self):
        template_folder = os.path.join(os.path.abspath(os.path.dirname(__file__)), "templates")
        static_folder = os.path.join(os.path.abspath(os.path.dirname(__file__)), "static")
        self.web.contexts.register("webmanager",
                                   template_folder=template_folder,
                                   static_folder=static_folder,
                                   url_prefix="/webmanager",
                                   description="context for web manager urls")

        self.web.routes.register("/", ["GET"], self.__manager_view, context="webmanager",
                                 name="manager_view", description="Entry-Page for the webmanager")

        self.web.routes.register("/command", ["GET"], self.__command_view, context="webmanager",
                                 name="command_list", description="Lists all registered commands")

        self.web.routes.register("/plugin", ["GET"], self.__plugin_view, context="webmanager",
                                 name="plugin_list", description="Lists all registered plugins")

        self.web.routes.register("/plugin/class/<clazz>", ["GET", "POST"], self.__plugin_class_view,
                                 context="webmanager",
                                 name="plugin_class_details", description="Shows details of a plugin class")

        self.web.routes.register("/plugin/instance/<plugin>", ["GET", "POST"], self.__plugin_detail_view,
                                 context="webmanager",
                                 name="plugin_details", description="Shows details of a plugin instance")

        self.web.routes.register("/route", ["GET"], self.__route_view, context="webmanager",
                                 name="route_list", description="Lists all registered routes")

        self.web.routes.register("/menu", ["GET"], self.__menu_view, context="webmanager",
                                 name="menu_list", description="Lists all registered menus")

        self.web.routes.register("/context", ["GET"], self.__context_view, context="webmanager",
                                 name="context_list", description="Lists all registered contexts")

        self.web.routes.register("/provider", ["GET"], self.__provider_view, context="webmanager",
                                 name="provider_list", description="Lists all registered providers")

        self.web.routes.register("/server", ["GET"], self.__server_view, context="webmanager",
                                 name="server_list", description="Lists all registered servers")

        webmanager_menu = self.web.menus.register("WebManager", "/webmanager")
        self.web.menus.register("Commands", "/webmanager/command", menu=webmanager_menu)
        self.web.menus.register("Plugins", "/webmanager/plugin", menu=webmanager_menu)
        self.web.menus.register("Routes", "/webmanager/route", menu=webmanager_menu)
        self.web.menus.register("Menu entries", "/webmanager/menu", menu=webmanager_menu)
        self.web.menus.register("Contexts", "/webmanager/context", menu=webmanager_menu)
        self.web.menus.register("Providers", "/webmanager/provider", menu=webmanager_menu)
        self.web.menus.register("Servers", "/webmanager/server", menu=webmanager_menu)

    def deactivate(self):
        self.commands.unregister("server_start")
        self.commands.unregister("server_list")

    def __server_start(self, server):
        servers = self.app.web.servers.get()
        if server not in servers.keys():
            echo("Server '%s' not found.")
            echo("Available servers: %s" % ",".join(servers.keys()))
        else:
            echo("Starting server %s" % server)
            servers[server].function()

    def __server_list(self):
        servers = self.app.web.servers.get()
        echo("List of registered servers\n")
        for name, server in servers.items():
            echo(name)
            echo("*"*len(name))
            echo("  Description: %s" % server.description)
            echo("  Plugin: %s" % server.plugin.name)

    def __manager_view(self):
        return self.web.providers.render("manager.html")

    def __command_view(self):
        return self.web.providers.render("commands.html", app=self.app)

    def __plugin_view(self):
        return self.web.providers.render("plugins.html", app=self.app)

    def __plugin_detail_view(self, plugin):
        plugin_instance = self.app.plugins.get(plugin)
        if plugin_instance is None:
            return "404"

        request = self.app.web.providers.default.instance.request
        if request.method == "POST":
            if plugin_instance.active:
                plugin_instance.deactivate()
            else:
                plugin_instance.activate()

        return self.web.providers.render("plugin_detail.html", app=self.app, plugin=plugin_instance)

    def __plugin_class_view(self, clazz):
        clazz_obj = self.app.plugins.classes.get(clazz)
        if clazz_obj is None:
            return "404"

        request = self.app.web.providers.default.instance.request
        if request.method == "POST":
            plugin_class = self.app.plugins.classes.get(clazz)
            name = request.form["name"] or clazz
            plugin_instance = self.app.plugins.initialise(plugin_class.clazz, name)

        return self.web.providers.render("plugin_class_detail.html", app=self.app, clazz=clazz_obj)

    def __route_view(self):
        routes = self.app.web.routes.get()
        return self.web.providers.render("routes.html", routes=routes, app=self.app)

    def __context_view(self):
        contexts = self.app.web.contexts.get()
        return self.web.providers.render("contexts.html", contexts=contexts)

    def __provider_view(self):
        providers = self.app.web.providers.get()
        return self.web.providers.render("providers.html", providers=providers)

    def __server_view(self):
        servers = self.app.web.servers.get()
        return self.web.providers.render("servers.html", servers=servers)

    def __menu_view(self):
        clusters = self.app.web.menus.get_clusters()

        menus = {}
        for cluster in clusters:
            menus[cluster] = self.app.web.menus.get(cluster=cluster)

        return self.web.providers.render("menus.html", menus=menus)


