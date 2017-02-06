import os
from click import Argument, echo

from groundwork.patterns import GwCommandsPattern


from groundwork_web.patterns import GwWebPattern


class GwWeb(GwWebPattern, GwCommandsPattern):
    def __init__(self, *args, **kwargs):
        self.name = kwargs.get("name", self.__class__.__name__)
        super(GwWeb, self).__init__(*args, **kwargs)

    def activate(self):
        self.commands.register("server_start", "starts a given server",
                               self.__server_start,
                               params=[Argument(("server",), required=True)])

        self.commands.register("server_list", "prints a list of registered server",
                               self.__server_list)

        template_folder = os.path.join(os.path.abspath(os.path.dirname(__file__)), "templates")
        static_folder = os.path.join(os.path.abspath(os.path.dirname(__file__)), "static")
        self.web.contexts.register("web",
                                   template_folder=template_folder,
                                   static_folder=static_folder,
                                   url_prefix="/",
                                   description="web context, which was created by GwWeb as initial context")

        if self.app.config.get("SHOW_WEB_TEST_PAGE", True):
            self.web.routes.register("/test", ["GET"], self.__test_view,
                                     name="Test", description="Test view of GwWeb")

        # Register the flask debug server.
        self.web.servers.register("flask_debug", self.__start_flask_debug_server, "Starts the flask debug server")

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
            echo("*" * len(name))
            echo("  Description: %s" % server.description)
            echo("  Plugin: %s" % server.plugin.name)

    def __start_flask_debug_server(self):

        host = str(self.app.config.get("FLASK_HOST", "127.0.0.1"))
        port = int(self.app.config.get("FLASK_PORT", 5000))
        server_name = str(self.app.config.get("FLASK_SERVER_NAME", "%s:%s" % ("127.0.0.1", port)))
        self.web.flask.config.SERVER_NAME = server_name

        self.log.info("Flask Server Name: %s" % self.web.flask.config["SERVER_NAME"])
        self.web.flask.run(host=host,
                           port=port,
                           debug=bool(self.app.config.get("FLASK_DEBUG", True)))

    def __test_view(self):
        return self.web.render("test.html")
