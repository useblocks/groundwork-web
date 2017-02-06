import os
from flask import request, url_for

from groundwork_web.patterns import GwWebPattern


class GwWebManager(GwWebPattern):
    """
    Provides functions and views to manage the application via a web interface.

    """
    def __init__(self, *args, **kwargs):
        self.name = kwargs.get("name", self.__class__.__name__)
        self.needed_plugins = ["GwWeb"]
        super(GwWebManager, self).__init__(*args, **kwargs)

    def activate(self):
        template_folder = os.path.join(os.path.abspath(os.path.dirname(__file__)), "templates")
        static_folder = os.path.join(os.path.abspath(os.path.dirname(__file__)), "static")
        self.web.contexts.register("webmanager",
                                   template_folder=template_folder,
                                   static_folder=static_folder,
                                   url_prefix="/webmanager",
                                   description="context for web manager urls")

        # Pure groundwork objects

        self.web.routes.register("/", ["GET"], self.__manager_view, context="webmanager",
                                 name="manager_view", description="Entry-Page for the webmanager")

        self.web.routes.register("/command", ["GET"], self.__command_view, context="webmanager",
                                 name="command_list", description="Lists all registered commands")

        self.web.routes.register("/plugin", ["GET"], self.__plugin_view, context="webmanager",
                                 name="plugin_list", description="Lists all registered plugins")

        self.web.routes.register("/plugin/class/<clazz>", ["GET", "POST"], self.__plugin_class_view,
                                 context="webmanager",
                                 name="plugin_class_details", description="Shows details of a plugin class")

        self.web.routes.register("/plugin/instance/<plugin_name>", ["GET", "POST"], self.__plugin_detail_view,
                                 context="webmanager",
                                 name="plugin_details", description="Shows details of a plugin instance")

        self.web.routes.register("/signal", ["GET"], self.__signal_view, context="webmanager",
                                 name="signal_list", description="Lists all registered signals")

        self.web.routes.register("/receiver", ["GET"], self.__receiver_view, context="webmanager",
                                 name="receiver_list", description="Lists all registered receivers")

        self.web.routes.register("/document", ["GET"], self.__document_view, context="webmanager",
                                 name="document_list", description="Lists all registered documents")

        # WEB objects

        self.web.routes.register("/route", ["GET"], self.__route_view, context="webmanager",
                                 name="route_list", description="Lists all registered routes")

        self.web.routes.register("/menu", ["GET"], self.__menu_view, context="webmanager",
                                 name="menu_list", description="Lists all registered menus")

        self.web.routes.register("/context", ["GET"], self.__context_view, context="webmanager",
                                 name="context_list", description="Lists all registered contexts")

        self.web.routes.register("/server", ["GET"], self.__server_view, context="webmanager",
                                 name="server_list", description="Lists all registered servers")

        with self.app.web.flask.app_context():
            webmanager_menu = self.web.menus.register("WebManager", "/webmanager")
            webmanager_menu.register("Overview", "/webmanager")
            webmanager_menu.register("Commands", url_for("webmanager.__command_view"))
            webmanager_menu.register("Signals", url_for("webmanager.__signal_view"))
            webmanager_menu.register("Receivers", url_for("webmanager.__receiver_view"))
            webmanager_menu.register("Plugins", url_for("webmanager.__plugin_view"))
            webmanager_menu.register("Routes", url_for("webmanager.__route_view"))
            webmanager_menu.register("Menu entries", url_for("webmanager.__menu_view"))
            webmanager_menu.register("Contexts", url_for("webmanager.__context_view"))
            webmanager_menu.register("Servers", url_for("webmanager.__server_view"))
            webmanager_menu.register("Documents", url_for("webmanager.__document_view"))

    def deactivate(self):
        pass

    def __manager_view(self):
        return self.web.render("manager.html")

    def __command_view(self):
        return self.web.render("commands.html")

    def __document_view(self):
        return self.web.render("documents.html")

    def __signal_view(self):
        return self.web.render("signals.html")

    def __receiver_view(self):
        return self.web.render("receivers.html")

    def __plugin_view(self):
        return self.web.render("plugins.html")

    def __plugin_detail_view(self, plugin_name):
        plugin_instance = self.app.plugins.get(plugin_name)
        if plugin_instance is None:
            return "404"

        if request.method == "POST":
            if plugin_instance.active:
                plugin_instance.deactivate()
            else:
                plugin_instance.activate()

        return self.web.render("plugin_detail.html", plugin_instance=plugin_instance)

    def __plugin_class_view(self, clazz):
        clazz_obj = self.app.plugins.classes.get(clazz)
        if clazz_obj is None:
            return "404"

        if request.method == "POST":
            plugin_class = self.app.plugins.classes.get(clazz)
            name = request.form["name"] or clazz
            self.app.plugins.initialise(plugin_class.clazz, name)

        return self.web.render("plugin_class_detail.html", clazz=clazz_obj)

    def __route_view(self):
        routes = self.app.web.routes.get()
        return self.web.render("routes.html", routes=routes)

    def __context_view(self):
        contexts = self.app.web.contexts.get()
        return self.web.render("contexts.html", contexts=contexts)

    def __provider_view(self):
        providers = self.app.web.providers.get()
        return self.web.render("providers.html", providers=providers)

    def __server_view(self):
        servers = self.app.web.servers.get()
        return self.web.render("servers.html", servers=servers)

    def __menu_view(self):
        clusters = self.app.web.menus.get_clusters()

        menus = {}
        for cluster in clusters:
            menus[cluster] = self.app.web.menus.get(cluster=cluster)

        return self.web.render("menus.html", menus=menus)
