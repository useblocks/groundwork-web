import json

from groundwork_web.patterns import GwWebDocPattern
from groundwork_web.plugins import GwWeb, GwWebManager, GwWebDoc


def test_web_doc_export(basicApp):

    class DocPlugin(GwWebDocPattern):
        def __init__(self, *args, **kwargs):
            self.name = self.__class__.__name__
            super(DocPlugin, self).__init__(*args, **kwargs)
            
        def activate(self):
            pass
        
        def deactivate(self):
            pass
    
    def _view():
        export = doc.export()
        assert export is not None
        
        export_json = json.dumps(export)
        return export_json

    plugin = DocPlugin(basicApp)
    plugin.activate()

    plugin.web.routes.register("/test_api", _view, name="test_route", description="test route", methods=["GET", "POST"])

    route = plugin.app.web.routes.get("test_route")

    doc = plugin.web.doc.register('test_doc', 'my test doc')
    assert doc is not None
    assert doc.name == 'test_doc'

    gw_web = GwWeb(basicApp)
    gw_web.activate()

    gw_webmanager = GwWebManager(basicApp)
    gw_webmanager.activate()

    gw_web_doc = GwWebDoc(basicApp)
    gw_web_doc.activate()
    

    
    



