.. image:: https://img.shields.io/pypi/l/groundwork-web.svg
   :target: https://pypi.python.org/pypi/groundwork-web
   :alt: License
.. image:: https://img.shields.io/pypi/pyversions/groundwork-web.svg
   :target: https://pypi.python.org/pypi/groundwork-web
   :alt: Supported versions
.. image:: https://readthedocs.org/projects/groundwork-web/badge/?version=latest
   :target: https://readthedocs.org/projects/groundwork-web/
.. image:: https://travis-ci.org/useblocks/groundwork-web.svg?branch=master
   :target: https://travis-ci.org/useblocks/groundwork-web
   :alt: Travis-CI Build Status
.. image:: https://coveralls.io/repos/github/useblocks/groundwork-web/badge.svg?branch=master
   :target: https://coveralls.io/github/useblocks/groundwork-web?branch=master
.. image:: https://img.shields.io/scrutinizer/g/useblocks/groundwork-web.svg
   :target: https://scrutinizer-ci.com/g/useblocks/groundwork-web/
   :alt: Code quality
.. image:: https://img.shields.io/pypi/v/groundwork-web.svg
   :target: https://pypi.python.org/pypi/groundwork-web
   :alt: PyPI Package latest release

.. _groundwork: https://groundwork.readthedocs.io

Welcome to groundwork web
=========================

groundwork-web provides web app management functions to applications based on the framework `groundwork`_.

This package contains the following applications, plugins or patterns:

Applications
------------
GroundworkWebApp
~~~~~~~~~~~~~~~~
Example application, which mainly loads the plugin gw_web and gw_web_manager

Plugins
-------
GwWeb
~~~~~
Provides command line commands to to show and start web servers. Configures also the web server "flask_debug".

GwWebManager
~~~~~~~~~~~~
Provides web views and functions to manage groundwork objects like commands, recipes, signals, web routes and more.
Allows the user to get a fast overview about the running applications and its configuration.

Patterns
--------
GwWebPattern
~~~~~~~~~~~~
Allows plugins to register web routes and servers.
Cares about the correct setup of flask, on which most groundwork web functions are based on.

GwWebDbAdminPattern
~~~~~~~~~~~~~~~~~~~
Allows the registration of database tables to provide admin web views for them.
This enables you to create, read, update and delete (CRUD) content of database tables via a web interface.

GwWebDbRestPattern
~~~~~~~~~~~~~~~~~~
Allows the registration of database tables to provide a REST interface for them.
This enables you to create, read, update and delete (CRUD) content of database tables via a REST interface.

Table of content
----------------

.. toctree::
   :maxdepth: 2

   installation
   architecture
   applications
   plugins
   patterns
   contribution