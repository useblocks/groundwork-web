GwWebPattern
============
Adds web related functions to plugins to allow their registration and configuration.

Web Servers
-----------
This function lets an developer integrate several servers with different configurations and make them easily available
via command line interface.

**use case**: There may be a special server for debug purposes and one for production, which is more secured.
Like `Flasks debug server <http://flask.pocoo.org/docs/0.12/server/>`_ for debugging and
`Pylons Waitress server <http://docs.pylonsproject.org/projects/waitress/en/latest/>`_ for production.


Registration
~~~~~~~~~~~~

To register a new web server::

    from groundwork_web.patterns import GwWebPattern
    import my_server

    class MyPlugin(GwWebPattern):
        def __init__(self):
            ...

        def activate(self):
            self.web.server.register("my_server", self.my_server_start, "starts my server")

        def my_server_start():
            print("Starting my server...")
            my_server.start()

Usage
~~~~~

As an example, we use the plugin :ref:`gwweb`, which uses the GwWebPattern to register a server for starting
the flask-debug server::

    >>> my_application server_list
    List of registered servers

    flask_debug
    ***********
      Description: Starts the flask debug server
      Plugin: GwWeb

    >>> my_application server_start flask_debug
    server_start flask_debug
    Starting server flask_debug
    * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)


Web Contexts
------------

Contexts are used to group routes and provide common folders for templates and static files.

.. note::

   groundwork contexts are based on flask blueprints.

The following code example is taken from the GwWebManager plugin::

    class GwWebManager(GwWebPattern):
    """
    Provides functions and views to manage the application via a web interface.

    """
    def __init__(self, *args, **kwargs):
        self.name = kwargs.get("name", self.__class__.__name__)
        self.needed_plugins = ["GwWeb"]
        super(GwWebManager, self).__init__(*args, **kwargs)

    def activate(self):
        # Calculate folder paths for template and static files
        template_folder = os.path.join(os.path.abspath(os.path.dirname(__file__)), "templates")
        static_folder = os.path.join(os.path.abspath(os.path.dirname(__file__)), "static")

        # Register a new context for webmanager views
        self.web.contexts.register("webmanager",
                                   template_folder=template_folder,
                                   static_folder=static_folder,
                                   url_prefix="/webmanager",
                                   description="context for web manager urls")

Web Routes
----------
Routes map view-functions to a specific url::

    # Code snippet from the activation routine of GwWebManager

    self.web.routes.register("/", ["GET"], self.__manager_view, context="webmanager",
                                 name="manager_view", description="Entry-Page for the webmanager")

    self.web.routes.register("/command", ["GET"], self.__command_view, context="webmanager",
                             name="command_list", description="Lists all registered commands")

    def __manager_view(self):
        return self.web.render("manager.html")

    def __command_view(self):
        return self.web.render("commands.html")


URL parameters
~~~~~~~~~~~~~~

You can define placeholders inside urls to dynamically care about a wide range of possible urls::

    # Code snippet from the activation routine of GwWebManager

    self.web.routes.register("/plugin/instance/<plugin_name>", ["GET", "POST"], self.__plugin_detail_view,
                                 context="webmanager",
                                 name="plugin_details", description="Shows details of a plugin instance")

    def __plugin_detail_view(self, plugin_name):
        plugin_instance = self.app.plugins.get(plugin_name)
        if plugin_instance is None:
            return "404"

        if request.method == "POST":
            if plugin_instance.active:
                plugin_instance.deactivate()
            else:
                plugin_instance.activate()

        return self.web.render("plugin_detail.html", plugin_instance=plugin_instance)

The used view-function must provide a parameter with the same name as the one used inside the url definition.


Web Menu Entries
----------------
Dynamically defining a menu structure can be a mess.

The GwWebPattern provides a way to easily register new menus and sub-menus.

The registered menu information can than be used inside templates to finally generate the menu design layout.

.. note::

   You should use the GwWeb plugin and its integrated base template, which already cares about the correct menu
   rendering on html pages.

Again the following code is part of the GwWeb plugin::

    with self.app.web.flask.app_context():
            # Register webmanager-menu
            webmanager_menu = self.web.menus.register("WebManager", "/webmanager")

            # Register sub-menus on the just registered webmanager-menu
            webmanager_menu.register("Overview", "/webmanager")
            webmanager_menu.register("Commands", url_for("webmanager.__command_view"))


.. note::

   ``with self.app.web.flask.app_context():`` is only needed, if you want to use flask's ``url_for`` function
   to calculate urls. Thats because flask can handle multiple apps in parallel and it needs to know, for which
   app it needs to calculate the url.


Rendering templates
-------------------

Jinja templates can be easil rendered by using ``self.web.render()``::

    return self.web.render("plugin_detail.html", plugin_instance=plugin_instance)

You are free to add own data via a keyword argument to it. Under the used name the data will be available inside
your template.