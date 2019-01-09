import os
import logging

from groundwork.util import gw_get


class RouteManagerPlugin:
    def __init__(self, plugin):
        self.plugin = plugin
        self.log = plugin.log
        self.app = plugin.app

    def register(self, url, endpoint=None, context=None, name=None, description=None, methods=None):
        return self.app.web.routes.register(url, self.plugin, endpoint, context, name, description, methods)


class RouteManagerApplication:
    def __init__(self, app):
        self._routes = {}
        self.app = app
        self.log = logging.getLogger(__name__)
        self.blueprints = {}

    def register(self, url, plugin, endpoint=None, context=None, name=None, description=None, methods=None):

        if endpoint is not None and context is None and self.app.web.contexts.default_context is None:
            self.log.warning("Context not given and no default context is available. Basic context will be created")
            basic_context = self.app.web.contexts.register("basic",
                                                           os.path.join(self.app.path, "template"),
                                                           os.path.join(self.app.path, "static"),
                                                           "/",
                                                           "basic context, which was created automatically due the "
                                                           "miss of an available context during first route "
                                                           "registration.",
                                                           plugin)
            context = basic_context.name

        if context is None:
            context_obj = self.app.web.contexts.default_context
        else:
            context_obj = self.app.web.contexts.get(context)

        if name is None:
            name = endpoint

        if name not in self._routes.keys():
            self._routes[name] = Route(url, context_obj, name, description, self.app,
                                       methods=methods, endpoint=endpoint, plugin=plugin)

        return self._routes[name]

    def get(self, name=None, plugin=None):
        return gw_get(self._routes, name, plugin)


class Route:
    """
    A single route, which gets mostly defined by supported methods and their parameters and responses
    """

    def __init__(self, url, context, name, description, app, methods=None, endpoint=None, plugin=None):
        self.url = url
        self.endpoint = endpoint
        self.context = context
        self.name = name
        self.description = description
        self.methods = {}
        self.plugin = plugin
        self.app = app
        self.log = logging.getLogger(__name__)

        if methods is None:
            methods = ['GET', ]

        for method in methods:
            if not isinstance(method, dict):  # If a string is given e.g. GET
                self.add_method(method)
            else:  # If a complex attribute is given
                self.add_method(**method)

        if endpoint is not None:
            blueprint = self.context.blueprint
            blueprint.add_url_rule(url, methods=methods, endpoint=endpoint.__name__, view_func=endpoint)
            # We have to (re-)register our blueprint to activate the route
            self.app.web.flask.register_blueprint(blueprint)

        self.log.info("Route registered:  %s for context %s (%s)" % (self.url, self.context.name,
                                                                     self.context.url_prefix))

    def add_method(self, name, description=None, parameters=None, responses=None, **kwargs):
        method = Method(name, description, parameters, responses, **kwargs)
        self.methods[method.name] = method
        return method

    def export(self, schema=None):
        if schema is None or schema == 'swagger_2':
            doc = {}
            for key, method in self.methods.items():
                doc[method.name.lower()] = method.export(schema)
        else:
            raise UnsupportedExportSchema('Export schema {} is not supported'.format(schema))

        return doc


class Method:
    """
    Supported method of a route, like GET, POST, OPTION, ...
    """

    def __init__(self, name, description=None, parameters=None, responses=None, **kwargs):
        self.name = name
        self.description = description

        self.parameters = []
        self.responses = []

        if parameters is None:
            parameters = []
        for parameter in parameters:
            self.add_parameter(**parameter)

        if responses is None:
            responses = []
        for response in responses:
            self.add_response(**response)

        for key, value in kwargs:
            setattr(self, key, value)

    def __repr__(self):
        return self.name

    def add_parameter(self, name, path_type, data_type, description, required=False,
                      default=None, minimum=None, maximum=None, **kwargs):
        """
        Adds a new parameter to the route
        :param name:
        :param path_type:
        :param data_type:
        :param description:
        :param required:
        :param default:
        :param minimum:
        :param maximum:
        :return:
        """
        parameter = Parameter(name, path_type, data_type, description, required, default, minimum, maximum, **kwargs)
        self.parameters.append(parameter)
        return parameter

    def add_response(self, name, description, content=None, **kwargs):
        """

        :param name:
        :param description:
        :param content:
        :param kwargs:
        :return:
        """
        response = Response(name, description, content, **kwargs)
        self.responses.append(response)
        return response

    def export(self, schema=None):
        if schema is None or schema == 'swagger_2':
            doc = {
                "description": self.description,
                "parameters": [],
                "responses": {}
            }
            for parameter in self.parameters:
                doc["parameters"].append(parameter.export(schema))

            for response in self.responses:
                doc['responses'][response.name] = response.export(schema)
        else:
            raise UnsupportedExportSchema('Export schema {} is not supported'.format(schema))

        return doc


class Parameter:
    """
    Supported Parameter for a given method
    """

    def __init__(self, name, path_type, data_type, description, required=False,
                 default=None, minimum=None, maximum=None, **kwargs):
        self.name = name
        self.path_type = path_type
        self.data_type = data_type
        self.description = description
        self.required = required
        self.default = default
        self.minimum = minimum
        self.maximum = maximum

        for key, value in kwargs:
            setattr(self, key, value)

    def export(self, schema=None):
        if schema is None or schema == 'swagger_2':
            doc = {
                "name": self.name,
                "in": self.path_type,
                "description": self.description,
                "required": self.required,
                "type": self.data_type
            }
        else:
            raise UnsupportedExportSchema('Export schema {} is not supported'.format(schema))

        return doc


class Response:
    """
    Supported Response of a method
    """

    def __init__(self, name, description, content=None, **kwargs):
        self.name = name
        self.description = description
        self.content = content

        for key, value in kwargs:
            setattr(self, key, value)

    def export(self, schema=None):
        if schema is None or schema == 'swagger_2':
            doc = {
                "description": self.description,
            }
        else:
            raise UnsupportedExportSchema('Export schema {} is not supported'.format(schema))

        return doc


class UnsupportedExportSchema(BaseException):
    """Schema for export is not supported"""
