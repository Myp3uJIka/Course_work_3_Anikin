from project.dao import UserDAO
from project.services.base import BaseService
from project.tools.security import generate_password_digest


class UsersService(BaseService):
    def get_by_email_password(self, data):
        data['password'] = generate_password_digest(data['password'])
        return UserDAO(self._db_session).get_by_email_password(data)

    def create(self, data):
        data['role'] = 'user'
        data['password'] = generate_password_digest(data['password'])
        return UserDAO(self._db_session).create(data)
