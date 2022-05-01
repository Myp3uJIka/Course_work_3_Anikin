from unittest.mock import patch, Mock, MagicMock

import pytest

from project.dao import DirectorDAO
from project.dao.models import Director
from project.schemas import DirectorSchema
from project.services import DirectorsService


class TestDirectorsService:
    @pytest.fixture(autouse=True)
    def service(self, db):
        self.service = DirectorsService(db.session)

    @pytest.fixture
    def director(self):
        return Director(id=1, name="director_1")

    @pytest.fixture
    def director_dao_mock(self, director):
        DirectorDAO.get_by_id = MagicMock(return_value=DirectorSchema().dump(director))
        DirectorDAO.get_all = MagicMock(return_value=DirectorSchema(many=True).dump([director]))
        return DirectorDAO

    def test_get_director_by_id(self, director_dao_mock, director):
        assert self.service.get_item_by_id(director.id) == DirectorSchema().dump(director)

    def test_get_all_directors(self, director_dao_mock, director):
        assert self.service.get_all_directors() == DirectorSchema(many=True).dump([director])
