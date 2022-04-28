from project.dao import UserDAO
from project.exceptions import ItemNotFound
from project.schemas.user import UserSchema
from project.services.base import BaseService
from project.tools.security import generate_password_digest


class UsersService(BaseService):
    def get_all(self):
        users = UserDAO(self._db_session).get_all()
        return UserSchema(many=True).dump(users)

    def get_one(self, u_id):
        user = UserDAO(self._db_session).get_one(u_id)
        if not user:
            raise ItemNotFound
        return UserSchema().dump(user)

    def get_by_email_password(self, data):
        data['password'] = generate_password_digest(data['password'])
        return UserDAO(self._db_session).get_by_email_password(data)

    def create(self, data):
        data['role'] = 'user'
        data['password'] = generate_password_digest(data['password'])
        return UserDAO(self._db_session).create(data)

    def update(self, data):
        user = UserDAO(self._db_session).get_one(data['id'])
        if 'email' in data:
            user.email = data['email']
        if 'password' in data:
            user.password = data['password']
        if 'name' in data:
            user.name = data['name']
        if 'surname' in data:
            user.surname = data['surname']
        if 'favourite_genre' in data:
            user.favorite_genre = data['favourite_genre']
        if 'role' in data:
            user.role = data['role']
        UserDAO(self._db_session).update(user)

    def get_user_password(self, u_id):
        user = UserDAO(self._db_session).get_one(u_id)
        return user.password
