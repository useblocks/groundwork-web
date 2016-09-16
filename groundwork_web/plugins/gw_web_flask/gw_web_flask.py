from flask import Flask, render_template, Blueprint
from groundwork.patterns import GwCommandsPattern

from groundwork_web.patterns import GwWebPattern
from groundwork_web.patterns.gw_web_pattern.provider import BaseProvider


class GwWebFlask(GwWebPattern, GwCommandsPattern):
    def __init__(self, *args, **kwargs):
        self.name = self.__class__.__name__
        super().__init__(*args, **kwargs)
        self.flask_app = None

    def activate(self):
        self.flask_app = Flask(__name__)

        # Inject send_signal() to jinja templates
        # Use it like {{ send_signal("my_signal") }}
        self.flask_app.jinja_env.globals.update(send_signal=self.signals.send)

        self.flask_app.jinja_env.globals.update(get_menu=self.__get_menu)

        self.flask_app.jinja_env.globals.update(get_config=self.app.config.get)

        # self.signals.register("web_menu", "signal to retrieve entries for the web menu")
        # self.signals.connect("test", "test_web", blub, description="test web signal")

        self.web.providers.register("flask", FlaskProvider(self.flask_app), "Flask web provider")
        self.web.servers.register("flask_debug", self.__start_flask_debug_server, "Starts the flask debug server")

    def deactivate(self):
        self.flask_app = None

    def __start_flask_debug_server(self):
        self.flask_app.run()

    def __get_menu(self, cluster="base"):
        return self.web.menus.get(cluster=cluster)


class FlaskProvider(BaseProvider):
    def __init__(self, instance, *args, **kwargs):
        self.flask_app = instance
        self.blueprints = {}

    def register_route(self, url, methods, endpoint, context, *arg, **kwargs):
        if context not in self.blueprints.keys():
            raise NameError("Context %s does not exist" % context)

        blueprint = self.blueprints[context]
        blueprint.add_url_rule(url, methods=methods, endpoint=endpoint.__name__, view_func=endpoint)

        # We have to register our blueprint to activate the route
        self.flask_app.register_blueprint(blueprint)

    def register_context(self, name, template_folder, static_folder, url_prefix, overwrite=False, *arg, **kwargs):
        if name in self.blueprints.keys() and not overwrite:
            raise NameError("Context %s already exists" % name)

        blueprint = Blueprint(name, __name__,
                              url_prefix=url_prefix,
                              subdomain=None,
                              template_folder=template_folder,
                              static_folder=static_folder,
                              static_url_path="/static/" + name)
        self.blueprints[name] = blueprint
        self.flask_app.register_blueprint(blueprint)

    def render(self, template, **kwargs):
        return render_template(template, **kwargs)

