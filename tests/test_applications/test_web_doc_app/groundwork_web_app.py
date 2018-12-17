import os
from groundwork import App
from groundwork_web.plugins import GwWebDoc
from tests.test_plugins.web_doc_plugin import WebDocTestPlugin


def start_app():
    app = register_app()
    app.commands.start_cli()


def register_app():
    app = App([os.path.join(os.path.dirname(__file__), "configuration.py")], strict=True)
    app.plugins.activate(app.config.PLUGINS)

    doc_plugin = GwWebDoc(app)
    doc_plugin.activate()

    plugin = WebDocTestPlugin(app)
    plugin.activate()
    return app


if __name__ == "__main__":  # pragma: no cover
    start_app()
