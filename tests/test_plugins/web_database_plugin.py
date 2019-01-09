from sqlalchemy import Column, Integer, String

from groundwork_web.patterns import GwWebDbAdminPattern, GwWebDbRestPattern


def _create_user_class(Base):
    class User(Base):
        __tablename__ = 'user'
        id = Column(Integer, primary_key=True)
        name = Column(String)
        fullname = Column(String)
        password = Column(String)

    return User


class WebDatabasePlugin(GwWebDbAdminPattern, GwWebDbRestPattern):
    def __init__(self, *args, **kwargs):
        self.name = kwargs.get("name", self.__class__.__name__)
        super(WebDatabasePlugin, self).__init__(*args, **kwargs)

    def activate(self):
        # my_db = self.databases.register("main", "sqlite:///:memory:", "main test database")
        my_db = self.databases.register("main", "sqlite:///test.db", "main test database")
        session = my_db.session
        session.autoflush = True

        User = _create_user_class(my_db.Base)
        my_User = my_db.classes.register(User)
        my_db.create_all()

        self.web.db.register(my_User.clazz, session)
        self.web.rest.register(my_User.clazz, session)

    def deactivate(self):
        pass
