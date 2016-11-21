from groundwork_web.patterns import GwWebDbAdminPattern

class WebDatabasePlugin(GwWebDbAdminPattern):
    def __init__(self, *args, **kwargs):
        self.name = kwargs.get("name", self.__class__.__name__)
        super().__init__(*args, **kwargs)

    def activate(self):
        pass

    def deactivate(self):
        pass
