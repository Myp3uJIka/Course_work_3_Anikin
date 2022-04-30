import pytest

from project.dao import UserDAO
from project.dao.models import User


class TestUsersDAO:
    @pytest.fixture(autouse=True)
    def dao(self, db):
        self.dao = UserDAO(db.session)

    @pytest.fixture
    def user_1(self, db):
        user = User(
            email="test1@mail.ru",
            password="qwerty123",
            name="John",
            surname="none",
            favorite_genre="5",
            role="user"
        )
        db.session.add(user)
        db.session.commit()
        return user

    @pytest.fixture
    def user_2(self, db):
        user = User(
            email="test2@mail.ru",
            password="qwerty321",
            name="Mary",
            surname="none",
            favorite_genre="2",
            role="user"
        )
        db.session.add(user)
        db.session.commit()
        return user

    def test_user_get_one(self, user_1):
        assert self.dao.get_one(user_1.id) == user_1

    def test_user_get_one_not_found(self):
        assert self.dao.get_one(1) is None

    def test_user_get_by_email_password(self, user_1):
        data = {
            "email": user_1.email,
            "password": user_1.password
        }
        assert self.dao.get_by_email_password(data) == user_1

    def test_user_get_all(self, user_1, user_2):
        assert self.dao.get_all() == [user_1, user_2]

    def test_user_create(self):
        user = {
            "email": "new@mail.ru",
            "password": "qwerty999",
            "name": "Lukas",
            "surname": "none",
            "favorite_genre": "1",
            "role": "user"
        }
        assert self.dao.create(user) is None

    def test_user_delete(self, user_1):
        assert self.dao.delete(1) is None

    def test_user_update(self, user_1):
        assert self.dao.update(user_1) is None


