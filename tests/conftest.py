import pytest
from groundwork_web.patterns import GwWebPattern

@pytest.fixture
def basicApp():
    """
    Loads a basic groundwork application and returns it.
    :return: app
    """
    from groundwork import App
    from tests.test_plugins.empty_plugin import EmptyPlugin

    app = App(plugins=[EmptyPlugin], strict=True)
    app.plugins.activate(["EmptyPlugin"])
    return app


@pytest.fixture
def EmptyPlugin():
    from tests.test_plugins.empty_plugin import EmptyPlugin
    return EmptyPlugin


@pytest.fixture
def WebPlugin():
    from tests.test_plugins.web_plugin import WebPlugin
    return WebPlugin

@pytest.fixture
def WebDatabasePlugin():
    from tests.test_plugins.web_database_plugin import WebDatabasePlugin
    return WebDatabasePlugin