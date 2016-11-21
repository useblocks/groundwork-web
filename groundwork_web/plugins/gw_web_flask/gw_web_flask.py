from docutils.core import publish_parts

from flask import Flask, render_template, Blueprint, request
from groundwork.patterns import GwCommandsPattern

from groundwork_web.patterns import GwWebPattern
from groundwork_web.patterns.gw_web_pattern.provider import BaseProvider


class GwWebFlask(GwWebPattern, GwCommandsPattern):
    def __init__(self, *args, **kwargs):
        self.name = kwargs.get("name", self.__class__.__name__)

        super().__init__(*args, **kwargs)
        self.flask_app = None

    def activate(self):
        self.flask_app = Flask(__name__)

        # Inject send_signal() to jinja templates
        # Use it like {{ send_signal("my_signal") }}
        self.flask_app.jinja_env.globals.update(send_signal=self.signals.send)

        self.flask_app.jinja_env.globals.update(get_menu=self.__get_menu)

        self.flask_app.jinja_env.globals.update(get_config=self.app.config.get)

        self.flask_app.jinja_env.globals.update(rst2html=self.__rst2html)

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

    def __rst2html(self, document, part="body"):
        if document is not None and type(document) == str:
            doc_rendered = publish_parts(document, writer_name="html")
            if part not in doc_rendered.keys():
                raise KeyError("%s is not a valid key for part parameter of rst2html.\nValid options: " %
                               (part, ",".join(doc_rendered.keys())))

            return doc_rendered[part]
        return document


class FlaskProvider(BaseProvider):
    """
    FlaskProvider, which maps general provider functions to flask specific functions and objects.

    For contexts, the flask blueprint mechanism is used and each router registration must provide a context.

    For render() flask's render_template() is used.

    The flask object itself is available under ``flask_app``. E.g. app.web.providers.get("flask").flask_app
    """

    def __init__(self, instance, *args, **kwargs):
        self.flask_app = instance
        self.blueprints = {}
        self.request = request

    def register_route(self, url, methods, endpoint, context, *arg, **kwargs):
        """
        Registers a route in flask.

        :param url: url for route, related to the context base url
        :param methods: List of allowed HTTP methods, e.g. ["GET", "POST"]
        :param endpoint: functions, which gets called, if route gets requested.
        :param context: The name of the context, under which the route shall be registered
        :param arg: Optional arguments
        :param kwargs: Optional key-word arguments
        :return: None
        """
        if context not in self.blueprints.keys():
            raise NameError("Context %s does not exist" % context)

        blueprint = self.blueprints[context]
        blueprint.add_url_rule(url, methods=methods, endpoint=endpoint.__name__, view_func=endpoint)

        # We have to (re-)register our blueprint to activate the route
        self.flask_app.register_blueprint(blueprint)

    def register_context(self, name, template_folder, static_folder, url_prefix, overwrite=False, *arg, **kwargs):
        """
        Registers a new context (aka blueprint in flask).

        :param name: Name of the context
        :param template_folder:  Location of the template folder
        :param static_folder:  Location of the static folder
        :param url_prefix: A prefix for all routes, which get registered for this context. E.G. url_prefix="/test",
        new route url = "my_page" --> url = /test/my_page
        :param overwrite: if True, an existing context gets overwritten without an error. Default is False
        :param arg: Optional arguments
        :param kwargs: Optional key-word arguments
        :return: None
        """
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
        """
        Renders a template and returns a strings, which represents the rendered data.

        Internally render_template() from flask is used.

        :param template: Name of the template
        :param kwargs: Optional key-word arguments, which get passed to the template engine.
        :return: Rendered template as string
        """

        return render_template(template, **kwargs)

