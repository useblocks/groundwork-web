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

By loading the plugin :ref:`gwweb` inside an groundwork application, you can easily start servers on command line or get a
list of all registered servers::

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




Web Routes
----------

Web Menu Entries
----------------

