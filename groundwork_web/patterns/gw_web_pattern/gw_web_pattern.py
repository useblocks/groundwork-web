import os
import logging
from flask import Flask, render_template
from docutils.core import publish_parts

from groundwork.patterns import GwBasePattern

from groundwork_web.patterns.gw_web_pattern.server import ServerManagerApplication, ServerManagerPlugin
from groundwork_web.patterns.gw_web_pattern.context import ContextManagerApplication, ContextManagerPlugin
from groundwork_web.patterns.gw_web_pattern.route import RouteManagerApplication, RouteManagerPlugin
from groundwork_web.patterns.gw_web_pattern.menu import MenuApplication, MenuPlugin


class GwWebPattern(GwBasePattern):

    def __init__(self, *args, **kwargs):
        super(GwWebPattern, self).__init__(*args, **kwargs)
        if not hasattr(self.app, "web"):
            self.app.web = WebApplication(self.app)

        #: Instance of :class:`~.WebPlugin`.
        #: Provides functions to manage web based objects
        self.web = WebPlugin(self)


class WebPlugin:
    def __init__(self, plugin):
        self.plugin = plugin
        self.app = plugin.app
        self.log = plugin.log

        self.servers = ServerManagerPlugin(plugin)
        self.contexts = ContextManagerPlugin(plugin)
        self.routes = RouteManagerPlugin(plugin)
        self.menus = MenuPlugin(plugin)

        self.plugin.signals.connect(receiver="%s_flask_activation" % self.plugin.name,
                                    signal="plugin_activate_pre",
                                    function=self.__init_flask,
                                    description="Initialised flask during plugin activation of %s" % self.plugin.name,
                                    sender=self.plugin)

    @property
    def flask(self):
        return self.app.web.flask

    @flask.setter
    def flask(self, value):
        self.app.web.flask = value

    def __init_flask(self, plugin, *args, **kwargs):
        self.app.web.init_flask()

    def render(self, template, plugin=None, **kwargs):
        if plugin is None:
            plugin = self.plugin

        return self.app.web.render(template, plugin, **kwargs)


class WebApplication:
    def __init__(self, app):
        self.app = app
        self.log = logging.getLogger(__name__)
        self.flask = None

        self.servers = ServerManagerApplication(app)
        self.contexts = ContextManagerApplication(app)
        self.routes = RouteManagerApplication(app)
        self.menus = MenuApplication(app)

    def init_flask(self):
        """
        Initialises and configures flask, is not already done,.
        :return: None
        """
        if self.flask is None:
            self.flask = Flask(self.app.name)

            # Inject send_signal() to jinja templates
            # Use it like {{ send_signal("my_signal") }}
            self.flask.jinja_env.globals.update(send_signal=self.app.signals.send)

            self.flask.jinja_env.globals.update(app=self.app)

            self.flask.jinja_env.globals.update(get_menu=self.__get_menu)
            self.flask.jinja_env.globals.update(get_config=self.app.config.get)
            self.flask.jinja_env.globals.update(rst2html=self.__rst2html)

            # Lets set the secret key for flask. This should be set in configuration files, so that
            # signed cookies are still valid if the server got restarted.
            # If there is no such parameter available, we create a temporary key, which is only
            # available during server runtime.
            self.flask.secret_key = self.app.config.get("FLASK_SECRET_KEY", os.urandom(24))

            self.flask.config["SERVER_NAME"] = self.app.config.get("FLASK_SERVER_NAME", "127.0.0.1:5000")
            self.log.info("Using FLASK_SERVER_NAME=%s" % self.flask.config.get("SERVER_NAME"))

    def __get_menu(self, cluster="base"):
        return self.menus.get(cluster=cluster)

    def __rst2html(self, document, part="body"):
        if document is not None and type(document) == str:
            doc_rendered = publish_parts(document, writer_name="html")
            if part not in doc_rendered.keys():
                raise KeyError("%s is not a valid key for part parameter of rst2html.\nValid options: " %
                               (part, ",".join(doc_rendered.keys())))
            return doc_rendered[part]
        return document

    def render(self, template, plugin=None, **kwargs):
        """
        Renders a template and returns a strings, which represents the rendered data.

        Internally render_template() from flask is used.

        :param template: Name of the template
        :param kwargs: Optional key-word arguments, which get passed to the template engine.
        :return: Rendered template as string
        """

        return render_template(template, app=self.app, plugin=plugin, **kwargs)
