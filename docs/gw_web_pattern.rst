GwWebPattern
============
Adds web related functions to plugins, to allow their registration and configuration.

Web Servers
-----------
Web servers can be registered to let a user easily start web servers via command line commands.

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

By loading the plugin "GwWeb" inside an groundwork application, you can easily start servers on command line or get a
list of all registered servers::

    my_application server_list
    my_application server_start my_server

Web Contexts
------------




Web Routes
----------

Web Menu Entries
----------------

