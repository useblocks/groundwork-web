.. _gwwebapp:

GroundworkWebApp
================

The gw_web_app is simple example application and loads mainly the plugins gw_web and gw_web_manager.

Command line
------------
Beside the groundwork default commands, the following commands are available::

* **server_list**: Shows a list of available server
* **server_start SERVER**: Starts a registered server with the name SERVER

Web servers
-----------
The following server names can be used to start the related web server:

* **flask_debug**: The flask internal debug server. Not production ready.

Web views
---------

* **Webmanager**: A collection of views and functions to manager and control groundwork basic and web functions.
  This includes:

  * plugins
  * signals
  * receivers
  * commands
  * documents
  * shared objects
  * recipes
  * web routes
  * web servers
  * web contexts
  * web menus


