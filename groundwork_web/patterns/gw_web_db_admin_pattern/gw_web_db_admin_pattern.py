import logging

from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from groundwork_web.util import get_routes

from groundwork_database.patterns import GwSqlPattern

from groundwork_web.patterns import GwWebPattern


class GwWebDbAdminPattern(GwWebPattern, GwSqlPattern):
    """
    Provides Views to create, read, update and delete database tables content.
    Based on `Flask-Admin <https://flask-admin.readthedocs.io/en/latest/>`_
    """

    def __init__(self, *args, **kwargs):
        super(GwWebDbAdminPattern, self).__init__(*args, **kwargs)
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

    def register(self, db_clazz, db_session):
        self.app.web.db.register(db_clazz, db_session, self.plugin)

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
        self.flask_admin = None
        self.context = None

    def register(self, db_clazz, db_session, plugin):
        """
        Adds a new class-based view to the flask-admin instance.

        :param plugin:
        :param db_clazz: SQLAlchemy class object
        :param db_session:  session object
        :return: Name of the endpoint, which can be used to generate urls for it.
        """
        # We must initialise the Flask-Admin class.
        # This can not be done during pattern initialisation, because Flask gets loaded and configured during
        # activation phase. So during initialisation it is not available.

        if self.flask_admin is None:
            self.flask_admin = Admin(self.app.web.flask,
                                     name=self.app.name,
                                     base_template="master.html",
                                     template_mode='bootstrap3')

        # After flask_admin initialisation, a first view/route got already registered.
        # We need to register this context as groundwork context as well.
        context = self.app.web.contexts.get('admin', None)
        if context is None:
            blueprint = self.flask_admin._views[0].blueprint
            if blueprint is not None:
                context = self.app.web.contexts.register(name='admin',
                                                         template_folder=blueprint.template_folder,
                                                         static_folder=blueprint.static_folder,
                                                         url_prefix=blueprint.url_prefix,
                                                         description='Admin panel context',
                                                         plugin=plugin,
                                                         blueprint=blueprint)

        url = "admin_%s" % db_clazz.__name__.lower()
        self.flask_admin.add_view(GroundworkModelView(db_clazz, db_session, endpoint=url))

        # for view in self.flask_admin._views:
        #     if view.endpoint == url:
        #         for route in view._urls:
        #             # _urls contains tuples: (url(str), description(str), methods(list of str))
        #             admin_url = "/" + url + route[0]
        #             admin_methods = route[2]
        #             self.app.web.routes.register(admin_url,
        #                                          admin_methods,
        #                                          plugin,
        #                                          name='_'.join([url, route[1]]),
        #                                          context=context.name)

        routes = get_routes(self.app.web.flask, url, context)
        for route in routes:
            self.app.web.routes.register(route['url'],
                                         plugin,
                                         methods=route['methods'],
                                         name=route['name'],
                                         context=route['context'])

        return url

    def unregister(self):
        pass

    def get(self):
        # REALLY needed?
        pass


class GroundworkModelView(ModelView):
    """
    Own ModelView for flask-admin, which defines some specific configuration for:

    * Showing primary key on list views

    """
    column_display_pk = True

    def __init__(self, *args, **kwargs):
        super(GroundworkModelView, self).__init__(*args, **kwargs)
