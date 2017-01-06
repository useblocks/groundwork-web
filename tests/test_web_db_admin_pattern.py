def test_web_db_admin(basicApp, WebDatabasePlugin):

    plugin = WebDatabasePlugin(basicApp)
    plugin.activate()

    my_plugin = plugin.app.plugins.get("WebDatabasePlugin")
    assert plugin == my_plugin
    assert plugin.active is True

    assert hasattr(plugin.web, "db") is True
    assert hasattr(plugin.app.web, "db") is True
