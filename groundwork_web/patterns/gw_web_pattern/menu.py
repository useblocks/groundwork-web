from groundwork.util import gw_get


class MenuPlugin:

    def __init__(self, plugin):
        self.plugin = plugin
        self.log = plugin.log
        self.app = plugin.app

    def register(self, name, link, icon=None, description=None, link_text=None, cluster="base", menu=None):
        return self.app.web.menus.register(name, link, self.plugin, icon, description, link_text, cluster, menu)

    def get(self, name=None, plugin=None, cluster="base"):
        return self.app.web.menus.get(name, plugin, cluster)


class MenuApplication:
    def __init__(self, app):
        self._routes = {}
        self.app = app
        self._menus = {"base": {}}

    def register(self, name, link, plugin, icon=None, description=None, link_text=None, cluster="base", menu=None):

        if menu is not None:
            return menu.register(name, link, plugin, icon, description, link_text)

        if cluster not in self._menus.keys():
            self._menus[cluster] = {}

        if name in self._menus[cluster].keys():
            raise NameError("menu %s already exists in cluster %s" % (name, cluster))

        self._menus[cluster][name] = Menu(name, link, plugin, icon, description, link_text)
        return self._menus[cluster][name]

    def get(self, name=None, plugin=None, cluster="base"):
        if cluster not in self._menus.keys():
            return {}

        return gw_get(self._menus[cluster], name, plugin)

    def get_clusters(self):
        return self._menus.keys()


class Menu:
    """
    """
    def __init__(self, name, link, plugin, icon=None, description=None, link_text=None):
        self.name = name
        self.link = link
        self.icon = icon
        self.description = description
        self.plugin = plugin

        if link_text is None:
            self.link_text = name
        else:
            self.link_text = link_text

        self.sub_menus = {}

    def register(self, name, link, plugin=None, icon=None, description=None, link_text=None):
        if name in self.sub_menus.keys():
            raise NameError("sub menu %s already exists for menu %s" % (name, self.name))

        if plugin is None:
            plugin = self.plugin

        self.sub_menus[name] = Menu(name, link, plugin, icon, description, link_text)
        return self.sub_menus[name]

    def unregister(self, name):
        if name not in self.sub_menus.keys():
            raise NameError("sub menu %s does not exist for menu %s" % (name, self.name))
        del(self.sub_menus[name])
