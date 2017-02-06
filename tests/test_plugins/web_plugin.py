from groundwork_web.patterns import GwWebPattern


class WebPlugin(GwWebPattern):
    def __init__(self, *args, **kwargs):
        self.name = kwargs.get("name", self.__class__.__name__)
        super(WebPlugin, self).__init__(*args, **kwargs)

    def activate(self):
        pass

    def deactivate(self):
        pass
