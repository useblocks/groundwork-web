from flask import Flask
from groundwork.patterns import GwCommandsPattern

from groundwork_web.patterns import GwWebPattern


class GwWebFlask(GwWebPattern, GwCommandsPattern):
    def __init__(self, *args, **kwargs):
        self.name = self.__class__.__name__
        super().__init__(*args, **kwargs)
        self.flask_app = None

    def activate(self):
        self.flask_app = Flask(__name__)
        self.web.providers.register("flask", self.flask_app, "Flask web provider")

        self.commands.register("webserver", "starts the flask debug server", self.__start_server)

    def deactivate(self):
        self.commands.unregister("webserver")
        self.flask_app = None

    def __start_server(self):
        self.flask_app.run()
