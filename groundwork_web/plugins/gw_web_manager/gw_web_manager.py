import os
from click import Argument, echo

from groundwork.patterns import GwCommandsPattern


from groundwork_web.patterns import GwWebPattern


class GwWebManager(GwWebPattern):
    def __init__(self, *args, **kwargs):
        self.name = self.__class__.__name__
        super().__init__(*args, **kwargs)

    def activate(self):
        template_folder = os.path.join(os.path.abspath(os.path.dirname(__file__)), "templates")
        static_folder = os.path.join(os.path.abspath(os.path.dirname(__file__)), "static")
        self.web.contexts.register("webmanager",
                                   template_folder=template_folder,
                                   static_folder=static_folder,
                                   url_prefix="/webmanager",
                                   description="context for web manager urls")

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
        self.web.menus.register("route", "/webmanager/route", menu=webmanager_menu)
        self.web.menus.register("menu", "/webmanager/menu", menu=webmanager_menu)
        self.web.menus.register("context", "/webmanager/context", menu=webmanager_menu)
        self.web.menus.register("provider", "/webmanager/provider", menu=webmanager_menu)
        self.web.menus.register("server", "/webmanager/server", menu=webmanager_menu)

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

    def __route_view(self):
        routes = self.app.web.routes.get()
        return self.web.providers.render("urls.html", urls=routes)

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


