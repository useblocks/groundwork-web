from sqlalchemy import Column, Integer, String

from groundwork_web.patterns import GwWebDbAdminPattern


class User(object):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    fullname = Column(String)
    password = Column(String)


class WebDatabasePlugin(GwWebDbAdminPattern):
    def __init__(self, *args, **kwargs):
        self.name = kwargs.get("name", self.__class__.__name__)
        super().__init__(*args, **kwargs)

        my_db = self.databases.register("main", "sqlite://", "main test database")
        my_User = my_db.classes.register(User)

        self.web.db.register(my_User, my_db.session)

    def activate(self):
        pass

    def deactivate(self):
        pass
