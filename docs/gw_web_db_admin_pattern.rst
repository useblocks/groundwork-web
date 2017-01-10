GwWebDbAdminPattern
===================

This pattern provides functions to easily create web interfaces to create and edit the content of database tables.

All you need is the database table object, which was created during its registration by the usage of the
GwDatabasePattern from the `groundwork-database <https://groundwork-database.readthedocs.io/en/latest/>`_ package.

Example
-------

In the following example we create a database and a related model by the help of the GwDatabasePattern.
To get the needed views to add and manipulate our database, we only need to add one line ``self.web.db.register(...)``,
which is provided by the GwWebDbAdminPattern.::


    from sqlalchemy import Column, Integer, String
    from groundwork_web.patterns import GwWebDbAdminPattern
    from groundwork_database.patterns import GwDatabasePattern

    class MyPlugin(GwWebDbAdminPattern, GwDatabasePattern):
        def __init__(self, *args, **kwargs):
            self.name = self.__class__.__name__
            super().__init__(*args, **kwargs)
            self.db = None

        def activate(self):
            """ Activation routine for our plugin """
            # Set up database
            self.db = self.app.databases.get("My_Database")

            # Get and register own database model
            MyUserTable = self.get_user_table(self.db)
            self.db.classes.register(MyUserTable)
            self.db.create_all()

            # Register model for new views
            self.web.db.register(MyUserTable, self.db.session)

        def get_user_table(database):
            """
            Helper function, which sets our database as base class
            and returns our model class
            """
            class MyUserTable(database):
                id = Column(Integer, primary_key=True)
                name = Column(String(255))

            return MyUserTable

Technical background
--------------------
groundwork-web uses the `Flask <http://flask.pocoo.org/>`_ extension
`Flask-Admin <https://flask-admin.readthedocs.io/en/latest/>`_ to provide this functionality.

The used Flask-Admin object is available under ``self.app.web.db.flask_admin`` and can be used to implement or activate
each documented functionality for Flask-Admin.
