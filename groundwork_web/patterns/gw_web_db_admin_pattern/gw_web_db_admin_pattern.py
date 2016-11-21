import logging

from flask_admin import Admin

from groundwork_database.patterns import GwSqlPattern

from groundwork_web.patterns import GwWebPattern
from groundwork_web.patterns.gw_web_db_admin_pattern.exceptions import FlaskNotFoundException


class GwWebDbAdminPattern(GwWebPattern, GwSqlPattern):
    """
    Provides Views to create, read, update and delete database tables content.
    Based on `Flask-Admin <https://flask-admin.readthedocs.io/en/latest/>`_
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not hasattr(self.app.web, "db"):
            self.app.web.db = WebDatabaseApplication(self.app)

        #: Instance of :class:`~.WebDatabasePlugin`.
        #: Provides functions to manage web based objects
        self.web.db = WebDatabasePlugin(self)


class WebDatabasePlugin:
    def __init__(self, plugin):
        self.plugin = plugin
        self.app = plugin.app
        self.log = plugin.log

        # Let's register a receiver, which cares about the deactivation process of web_databases for this plugin.
        # We do it after the original plugin deactivation, so we can be sure that the registered function is the last
        # one which cares about web_databases for this plugin.
        self.plugin.signals.connect(receiver="%s_web_db_deactivation" % self.plugin.name,
                                    signal="plugin_deactivate_post",
                                    function=self.__deactivate_web_db,
                                    description="Deactivates web databases for %s" % self.plugin.name,
                                    sender=self.plugin)
        self.log.debug("Pattern web database initialised")

    def register(self):
        pass

    def unregister(self):
        pass

    def get(self):
        # REALLY needed?
        pass

    def __deactivate_web_db(self, plugin, *args, **kwargs):
        pass


class WebDatabaseApplication:
    def __init__(self, app):
        self.app = app
        self.log = logging.getLogger(__name__)

        self._flask_provider = None
        self._flask_admin = None

    def register(self):
        # We must initialise the Flask-Admin class.
        # This can not be done during pattern initialisation, because Flask gets loaded and configured during
        # activation phase. So during initialisation it is not available.
        #

        if self._flask_provider is None:
            flask_provider = self.app.web.providers.get("flask")
            if flask_provider is None:
                raise FlaskNotFoundException("A Flask-Provider must be loaded. Please make sure plugin "
                                             "GwWebFlask got already loaded")
            self._flask_provider = flask_provider
            self._flask_admin = Admin(self._flask_provider.flask_app, name=self.app.name, template_mode='bootstrap3')

    def unregister(self):
        pass

    def get(self):
        # REALLY needed?
        pass





