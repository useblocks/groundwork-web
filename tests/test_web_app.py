from click.testing import CliRunner
from groundwork_web.applications import groundwork_web_app


def test_gw_app_start():
    runner = CliRunner()
    app = groundwork_web_app.register_app()
    runner.invoke(app.commands._click_root_command)
