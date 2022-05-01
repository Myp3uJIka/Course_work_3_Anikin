from unittest.mock import MagicMock

import pytest

from project.dao import UserDAO
from project.dao.models import User
from project.schemas import UserSchema
from project.services import UsersService


class TestUsersService:
    @pytest.fixture(autouse=True)
    def service(self, db):
        self.service = UsersService(db.session)

    @pytest.fixture
    def user(self):
        return User(
            email="test_user@mail.ru",
            password="asdfghjk1",
            name="none",
            surname="none",
            favorite_genre="1",
            role="user"
        )

    @pytest.fixture
    def user_dao_mock(self, user):
        UserDAO.get_one = MagicMock(return_value=user)
        UserDAO.get_by_email_password = MagicMock(return_value=UserSchema().dump(user))
        UserDAO.get_all = MagicMock(return_value=UserSchema(many=True).dump([user]))
        UserDAO.create = MagicMock()
        UserDAO.delete = MagicMock()
        UserDAO.update = MagicMock()

    def test_user_get_all(self, user_dao_mock, user):
        assert self.service.get_all() == UserSchema(many=True).dump([user])

    def test_user_get_one(self, user_dao_mock, user):
        assert self.service.get_one(user.id) == UserSchema().dump(user)

    def test_user_get_by_email_password(self, user_dao_mock, user):
        data = {
            "email": user.email,
            "password": user.password
        }
        assert self.service.get_by_email_password(data) == UserSchema().dump(user)

    def test_user_create(self, user_dao_mock):
        new_user = {
            "email": "test_user@mail.ru",
            "password": "asdfghjk1",
            "name": "none",
            "surname": "none",
            "favorite_genre": "1"
        }
        assert self.service.create(new_user) is None

    def test_user_update(self, user_dao_mock, user):
        update_user = {
            "id": "1",
            "email": "Test",
            "password": "Test",
            "name": "Test",
            "surname": "Test",
            "favorite_genre": "1"
        }
        assert self.service.update(update_user) is None
