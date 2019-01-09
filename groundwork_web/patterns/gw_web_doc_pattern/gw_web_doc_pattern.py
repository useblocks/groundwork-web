import logging
import re

from groundwork.util import gw_get
from groundwork_web.patterns import GwWebPattern
from groundwork_web.patterns.gw_web_pattern.route import UnsupportedExportSchema


class GwWebDocPattern(GwWebPattern):
    """
    Creates documentation objects of definable routes
    """

    def __init__(self, *args, **kwargs):
        super(GwWebDocPattern, self).__init__(*args, **kwargs)
        if not hasattr(self.app.web, "WebDocApplication"):
            self.app.web.doc = WebDocApplication(self.app)

        self.web.doc = WebDocPlugin(self)


class WebDocPlugin:
    def __init__(self, plugin):
        self.plugin = plugin
        self.app = plugin.app
        self.log = plugin.log

        self.log.debug("Pattern web doc initialised")

    def register(self, name, description, patterns=None, routes=None):
        return self.app.web.doc.register(name, description, self.plugin, patterns=patterns, routes=routes)

    def add_route(self, doc_name, route_name):
        pass

    def get(self, name=None):
        return self.app.web.doc.get(name, self.plugin)


class WebDocApplication:
    def __init__(self, app):
        self.app = app
        self.log = logging.getLogger(__name__)

        self.docs = {}

    def register(self, name, description, plugin, patterns=None, routes=None):
        if name in self.docs.keys():
            raise DocExistsException('Web document {} has been already registered by {}'.format(
                name, self.plugin.name
            ))

        self.docs[name] = Document(name, description, plugin, self.app, routes=routes, patterns=patterns)
        return self.docs[name]

    def add_route(self, doc_name, route_name):
        docs = self.get(route_name)

        if docs and len(docs) == 1:
            docs.add_route(route_name)

    def get(self, name=None, plugin=None):
        return gw_get(self.docs, name, plugin)


class Document:
    def __init__(self, name, description, plugin, app, routes=None, patterns=None):
        self.name = name
        self.description = description
        self.plugin = plugin
        self.app = app
        if routes is None:
            self.routes = {}
        else:
            self.routes = routes

        if patterns is not None:
            self.add_route_by_pattern(patterns)

    def add_route(self, name):
        if name not in self.routes.keys():
            route = self.app.web.routes.get(name, None)
            if route is None:
                raise UnknownRouteException('Route {} could not be added.'.format(name))
            self.routes[name] = route

    def add_route_by_pattern(self, patterns):
        if not isinstance(patterns, list):
            patterns = [patterns]

        for pattern in patterns:
            routes = self.app.web.routes.get()
            for key, route in routes.items():
                result = re.match(pattern, route.url)
                if result is not None and route.name not in self.routes:
                    self.routes[route.name] = route

    def export(self, schema=None):

        if schema is None or schema == 'swagger_2':
            doc = {
                "swagger": "2.0",
                "info": {
                    "title": self.name,
                    "description": self.description,
                    "version": "v2"
                },
                "host": '',
                'basePath': '',
                'schemes': [
                    'http'
                ],
                "paths": {},
                "consumes": [
                    "application/json"
                ]

            }

            for key, route in self.routes.items():
                doc['paths'][route.url] = route.export(schema)
        else:
            raise UnsupportedExportSchema('Export schema {} is not supported'.format(schema))

        return doc


class DocExistsException(BaseException):
    """Web Document already exists"""


class UnknownRouteException(BaseException):
    """Web Document already exists"""
