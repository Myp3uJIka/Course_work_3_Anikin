from sqlalchemy.orm import scoped_session

from project.dao.models import User


class UserDAO:
    def __init__(self, session: scoped_session):
        self._db_session = session

    def get_one(self, uid):
        return self._db_session.query(User).get(uid)

    def get_by_email_password(self, user):
        return self._db_session.query(User).filter(
            User.email == user['email'],
            User.password == user['password']
        ).one()

    def get_all(self):
        return self._db_session.query(User).all()

    def create(self, new_user):
        user = User(**new_user)
        self._db_session.add(user)
        self._db_session.commit()

    def delete(self, uid):
        user = self.get_one(uid)
        self._db_session.delete(user)
        self.commit()

    def update(self, user_update):
        user = self._db_session.query(User).filter(User.email == user_update['email']).one()
        user.id = user_update['id']
        user.email = user_update['email']
        user.name = user_update['name']
        user.surname = user_update['surname']
        user.favorite_genre = user_update['favorite_genre']
        user.role = user_update['role']

        self._db_session.commit()
