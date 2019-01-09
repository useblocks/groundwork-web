from groundwork_web.patterns import GwWebDocPattern
from flask_swagger_ui import get_swaggerui_blueprint


class GwWebDoc(GwWebDocPattern):
    def __init__(self, *args, **kwargs):
        self.name = kwargs.get("name", self.__class__.__name__)
        super(GwWebDoc, self).__init__(*args, **kwargs)

    def activate(self):
        SWAGGER_URL = "/test_doc"
        API_URL = "/test_api"
        swaggerui_blueprint = get_swaggerui_blueprint(
            SWAGGER_URL,  # Swagger UI static files will be mapped to '{SWAGGER_URL}/dist/'
            API_URL,
            config={  # Swagger UI config overrides
                'app_name': "Test application"
            },
        )

        # Register blueprint at URL
        # (URL must match the one given to factory function above)
        self.app.web.flask.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

    def deactivate(self):
        pass
