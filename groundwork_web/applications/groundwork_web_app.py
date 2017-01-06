import os
from groundwork import App


def start_app():
    app = register_app()
    app.commands.start_cli()


def register_app():
    app = App([os.path.join(os.path.dirname(__file__), "configuration.py")], strict=True)
    app.plugins.activate(app.config.PLUGINS)
    return app


if __name__ == "__main__":  # pragma: no cover
    start_app()
