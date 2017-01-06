# Test gw_web_pattern
def test_web_pattern(basicApp, WebPlugin):
    plugin = WebPlugin(basicApp)
    plugin.activate()

    assert basicApp.plugins.get("WebPlugin") is not None
    assert plugin.active is True

    assert hasattr(basicApp, "web") is True


def test_web_servers(basicApp, WebPlugin):

    def _test_server_start():
        return "started"

    plugin = WebPlugin(basicApp)
    plugin.activate()

    plugin.web.servers.register("server_start", _test_server_start, "start test server")

    server = plugin.app.web.servers.get("server_start")
    assert server is not None
    assert server.name == "server_start"
    assert server.function() == "started"


def test_web_contexts(basicApp, WebPlugin, tmpdir):

    plugin = WebPlugin(basicApp)
    plugin.activate()

    template_folder = tmpdir.mkdir("template")
    static_folder = tmpdir.mkdir("static")

    plugin.web.contexts.register("test_context", str(template_folder), str(static_folder), "/test", "test context")

    context = plugin.app.web.contexts.get("test_context")
    assert context is not None
    assert context.name == "test_context"
    assert context.template_folder == template_folder
    assert context.static_folder == static_folder
    assert context.url_prefix == "/test"
    assert context.description == "test context"
    assert context.plugin == plugin


def test_web_routes(basicApp, WebPlugin):

    def _view():
        pass

    plugin = WebPlugin(basicApp)
    plugin.activate()

    plugin.web.routes.register("/", ["GET", "POST"], _view, name="test_route", description="test route")

    route = plugin.app.web.routes.get("test_route")

    assert route is not None
    assert route.url == "/"
    assert route.methods == ["GET", "POST"]
    assert route.endpoint == _view
    assert route.context == plugin.app.web.contexts.default_context
    assert route.name == "test_route"
    assert route.description == "test route"


def test_web_menus(basicApp, WebPlugin):
    plugin = WebPlugin(basicApp)
    plugin.activate()

    menu_level_1 = plugin.web.menus.register("level_1_menu", "level_1")
    menu_level_2 = menu_level_1.register("level_2_menu", "level_2")
    assert plugin.app.web.menus.get("level_1_menu") == menu_level_1
    assert plugin.app.web.menus.get("level_1_menu").sub_menus["level_2_menu"] == menu_level_2

    # Cluster tests
    menu_level_1_a = plugin.web.menus.register("level_1_menu", "level_1", cluster="a")
    menu_level_2_a = menu_level_1_a.register("level_2_menu", "level_2")
    assert plugin.app.web.menus.get("level_1_menu", cluster="a") == menu_level_1_a
    assert plugin.app.web.menus.get("level_1_menu", cluster="a").sub_menus["level_2_menu"] == menu_level_2_a
