import json
from groundwork_web.patterns import GwWebDocPattern, GwWebDbRestPattern
from flask import make_response


class WebDocTestPlugin(GwWebDocPattern, GwWebDbRestPattern):
    def __init__(self, *args, **kwargs):
        self.name = kwargs.get("name", self.__class__.__name__)
        super(WebDocTestPlugin, self).__init__(*args, **kwargs)

    def activate(self):
        self.web.routes.register("/test_api", self._view, name="test_route", description="test route",
                                 methods=["GET", "POST"])
        # route = self.app.web.routes.get("test_route")

        doc = self.web.doc.register('test_doc', 'my test doc')
        doc.add_route_by_pattern('.')
        assert doc is not None
        assert doc.name == 'test_doc'

    def deactivate(self):
        pass

    def _view(self):
        doc = self.web.doc.get('test_doc')
        assert doc is not None

        export_json = json.dumps(doc.export(), indent=4)
        response = make_response(export_json)
        response.mimetype = 'application/json'
        return response
