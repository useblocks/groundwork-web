import logging

from flask_restless import APIManager

from groundwork_web.util import get_routes

from groundwork_database.patterns import GwSqlPattern

from groundwork_web.patterns import GwWebPattern


class GwWebDbRestPattern(GwWebPattern, GwSqlPattern):
    """
    Provides REST APIs for database tables.
    Based on `Flask-Restless <https://flask-restless.readthedocs.io/en/stable/>`_
    """

    def __init__(self, *args, **kwargs):
        super(GwWebDbRestPattern, self).__init__(*args, **kwargs)
        if not hasattr(self.app.web, "rest"):
            self.app.web.rest = WebRestApplication(self.app)

        #: Instance of :class:`~.WebRestPlugin`.
        #: Provides functions to manage web based objects
        self.web.rest = WebRestPlugin(self)


class WebRestPlugin:
    def __init__(self, plugin):
        self.plugin = plugin
        self.app = plugin.app
        self.log = plugin.log

        # Let's register a receiver, which cares about the deactivation process of web_databases for this plugin.
        # We do it after the original plugin deactivation, so we can be sure that the registered function is the last
        # one which cares about web_databases for this plugin.
        self.plugin.signals.connect(receiver="%s_web_rest_deactivation" % self.plugin.name,
                                    signal="plugin_deactivate_post",
                                    function=self.__deactivate_web_rest,
                                    description="Deactivates web rest apis for %s" % self.plugin.name,
                                    sender=self.plugin)
        self.log.debug("Pattern web rest initialised")

    def register(self, db_clazz, db_session, methods=None, collection_name=None):
        self.app.web.rest.register(db_clazz, db_session, self.plugin, methods, collection_name)

    def unregister(self):
        pass

    def __deactivate_web_rest(self, plugin, *args, **kwargs):
        pass


class WebRestApplication:
    def __init__(self, app):
        self.app = app
        self.log = logging.getLogger(__name__)
        self.flask_restless = None

    def register(self, db_clazz, db_session, plugin, methods=None, collection_name=None):
        """
        Adds a new class-based view to the flask-admin instance.

        :param plugin: plugin which has registered the api
        :param methods: supported HTTP methods
        :param collection_name:
        :param db_clazz: SQLAlchemy class object
        :param db_session:  session object
        :return: Name of the endpoint, which can be used to generate urls for it.
        """
        # We must initialise the Flask-restless class.
        # This can not be done during pattern initialisation, because Flask gets loaded and configured during
        # activation phase. So during initialisation it is not available.
        if self.flask_restless is None:
            self.flask_restless = APIManager(self.app.web.flask, session=db_session)

        if methods is None:
            methods = ["GET", "POST", "DELETE", "PATCH", "PUT"]

        if collection_name is None:
            collection_name = db_clazz.__name__.lower()
        self.flask_restless.create_api(db_clazz, methods=methods, collection_name=collection_name)

        blueprint = self.app.web.flask.blueprints[collection_name + 'api0']
        context = self.app.web.contexts.get('api', None)
        if blueprint is not None and context is None:
            context = self.app.web.contexts.register(name='api',
                                                     template_folder=blueprint.template_folder,
                                                     static_folder=blueprint.static_folder,
                                                     url_prefix=blueprint.url_prefix,
                                                     description='api panel context',
                                                     plugin=plugin,
                                                     blueprint=blueprint)

        routes = get_routes(self.app.web.flask, collection_name, context)

        for route in routes:
            reg_route = self.app.web.routes.register(route['url'],
                                                     plugin,
                                                     methods=route['methods'],
                                                     name=route['name'],
                                                     context=route['context'])

            for key, method in reg_route.methods.items():
                for key, param in route['parameters'].items():
                    method.add_parameter(name=param['name'],
                                         data_type=param['type'],
                                         description=param['description'],
                                         path_type='path')

    def unregister(self):
        pass
